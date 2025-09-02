from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Order, Order_items
from cart_app.models import Cart, Cart_items, Default_address
from product_app.models import Products, Product_image, Discount
# ------------------------
# Place Order
# ------------------------
@login_required
def placed_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = Cart_items.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(
                request,
                f"Cannot order {item.product.p_name}. Only {item.product.stock} items available."
            )
            return redirect('view_cart')

    if request.method == "POST":
        payment_method = request.POST.get('payment_method')
        default_address = Default_address.objects.get(user=request.user)

        # Set payment status based on method
        if payment_method != "Cash on Delivery":
            payment_status = "Paid"
        else:
            payment_status = "Pending"
            
        order = Order.objects.create(
            user=request.user,
            address=default_address.address,
            total_quantity=cart.total_quantity,
            order_amount=cart.total_mrp,
            order_savings=cart.total_discount,
            delivery_charge=cart.shipping,
            platform_fee=cart.platform_fee,
            total_amount=cart.final_total,
            payment_method=payment_method,
            payment_status=payment_status # Use the newly determined status
        )

        for item in cart_items:
            # Set initial item payment status
            item_payment_status = "Paid" if payment_status == "Paid" else "Pending"

            Order_items.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                amount=item.price,
                total_amount=item.price * item.quantity,
                image=item.image,
                payment_status=item_payment_status,
            )

            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()
        messages.success(request, "Order placed successfully!")
        return redirect('successful_order')

    return render(request, 'user/order/payment_details.html', {'cart': cart})


# ------------------------
# Order Success
# ------------------------
@login_required
def successful_order(request):
    return render(request, 'user/order/successful_order.html')

# ------------------------
# User Orders List
# ------------------------
@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    today = timezone.now().date()
    return render(request, 'user/order/orders.html', {"orders": orders,"today":today})

# ------------------------
# User Order Details
# ------------------------
@login_required
# ------------------------
# User Order Details
# ------------------------
@login_required
def order_details(request, id):
    order = get_object_or_404(Order, user=request.user, order_id=id)
    order_items = Order_items.objects.filter(order=order)

    # No need for manual status updates here, the model's save method handles it.
    
    context = {
        "order": order,
        "order_items": order_items,
    }
    return render(request, 'user/order/order_details.html', context)
# order_app/views.py
# ... other imports

# ------------------------
# Cancel Order Item Request
# ------------------------
@login_required
def cancel_order(request, item_id):
    order_item = get_object_or_404(Order_items, id=item_id, order__user=request.user)

    # Check if the item can be cancelled
    # Change the condition to only allow cancellation for "Pending" status
    if order_item.delivery_status == "Pending":
        order_item.delivery_status = "Cancellation Requested"
        order_item.refund_status = "Not Requested"

        if order_item.order.payment_method != "Cash on Delivery":
            order_item.payment_status = "Refund Requested"
            messages.success(request, "Cancellation and refund have been requested.")
        else:
            order_item.payment_status = "Cancelled"
            messages.success(request, "Cancellation has been requested.")
        
        order_item.save()
    else:
        messages.error(request, "This item cannot be cancelled.")

    return redirect('order_details', id=order_item.order.order_id)
# ------------------------
# Return Request
# ------------------------
@login_required
def request_return(request, item_id):
    order_item = get_object_or_404(Order_items, id=item_id, order__user=request.user)
    
    # Check if the item is eligible for return
    if order_item.can_return() and order_item.refund_status == "Not Requested":
        order_item.delivery_status = "Return Requested"
        order_item.payment_status = "Refund Requested"
        order_item.refund_status = "Requested"
        order_item.save()
        messages.success(request, "Return requested successfully.")
    else:
        messages.error(request, "This item is not eligible for return.")
    
    return redirect('order_details', id=order_item.order.order_id)