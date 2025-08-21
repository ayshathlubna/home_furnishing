from django.shortcuts import render,redirect
from .models import Order,Order_items
from cart_app.models import Cart,Cart_items,Default_address
from django.contrib import messages

# Create your views here.

def placed_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = Cart_items.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    if request.method == "POST":
        payment_method = request.POST.get('payment_method')

        default_address = Default_address.objects.get(user=request.user)
        # Create the order
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

        # Create order items
        for item in cart_items:
            Order_items.objects.create(
                order=order,  # link to order, not cart
                product=item.product,
                quantity=item.quantity,
                amount=item.price,
                total_amount=item.price * item.quantity,
                image = item.image 
            )

        # Empty the cart
        cart_items.delete()

        return redirect('successful_order')

    return render(request, 'user/order/payment_details.html')

def successful_order(request):
    cart = Cart.objects.get(user=request.user)
    return render(request,'user/order/successful_order.html')

def orders(request):
    order = Order.objects.filter(user=request.user).order_by('-order_date')
   
    if not order.exists():
        messages.info(request, "No orders created yet.")
        return render(request, 'user/order/orders.html')

    # Get all items belonging to these orders

    return render(request, 'user/order/orders.html', locals())

def order_details(request,id):
    order = Order.objects.get(user=request.user,order_id=id)
    order_items = Order_items.objects.filter(order=order)
    return render(request,'user/order/order_details.html',locals())