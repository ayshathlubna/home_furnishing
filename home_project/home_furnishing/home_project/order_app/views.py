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
@login_required
def placed_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = Cart_items.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    # Check stock availability
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

        order = Order.objects.create(
            user=request.user,
            address=default_address.address,
            total_quantity=cart.total_quantity,
            order_amount=cart.total_mrp,
            order_savings=cart.total_discount,
            delivery_charge=cart.shipping,
            platform_fee=cart.platform_fee,
            total_amount=cart.final_total,
            payment_method=payment_method
        )

        for item in cart_items:
            Order_items.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                amount=item.price,
                total_amount=item.price * item.quantity,
                image=item.image
            )

            # Reduce stock
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
def order_details(request, id):
    order = get_object_or_404(Order, user=request.user, order_id=id)
    order_items = Order_items.objects.filter(order=order)

    current_date = timezone.now().date()
    partially_refunded = False

    for item in order_items:
        # Initialize flags
        item.can_return_now = False
        item.can_cancel_now = False
        item.cancellation_requested = False  # <-- New flag

        # Return eligibility: delivered and within 7 days
        if item.delivery_status == "Delivered":
            if item.delivery_date:
                delta_days = (current_date - item.delivery_date).days
                if delta_days <= 7:
                    item.can_return_now = True

        # Cancel eligibility: pending and not refunded
        if item.delivery_status == "Pending" and item.refund_status == "Not Requested":
            item.can_cancel_now = True

        # Check if cancellation is requested
        if item.refund_status == "cancellation_requested":
            item.cancellation_requested = True

    # Partially refunded check
    total_items = order_items.count()
    refunded_items = order_items.filter(refund_status="Completed").count()
    if 0 < refunded_items < total_items:
        partially_refunded = True

    # Update order refund status automatically
    if refunded_items == total_items:
        order.refund_status = "Completed"
        order.save()
    elif partially_refunded:
        order.refund_status = "Partially Refunded"
        order.save()

    context = {
        "order": order,
        "order_items": order_items,
        "partially_refunded": partially_refunded,
    }
    return render(request, 'user/order/order_details.html', context)

# ------------------------
# Cancel Order Item Request
# ------------------------
@login_required
def cancel_order(request, item_id):
    order_item = get_object_or_404(Order_items, id=item_id, order__user=request.user)
    if order_item.delivery_status == "Pending" and order_item.refund_status == "Not Requested":
        order_item.refund_status = "cancellation_requested"
        order_item.save()
    return redirect('order_details', id=order_item.order.order_id)


# ------------------------
# Return Request
@login_required
def request_return(request, item_id):
    order_item = get_object_or_404(Order_items, id=item_id, order__user=request.user)
    if order_item.can_return_now and order_item.refund_status == "not_requested":
        order_item.refund_status = "return_requested"
        order_item.save()
        messages.success(request, "Return requested successfully.")
    return redirect('order_details', id=order_item.order.order_id)
