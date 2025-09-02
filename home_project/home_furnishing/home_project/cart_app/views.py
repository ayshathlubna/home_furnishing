
from django.shortcuts import render, redirect,get_object_or_404
from .models import Cart,Wishlist,Address,Default_address,Cart_items
from product_app.models import Products, Discount,Product_image
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from decimal import Decimal
from user_app.utils import weighted_hybrid_recommendations
from django.contrib import messages

@login_required
def add_to_cart(request, product_id):
    product = Products.objects.get(p_id=product_id)
    if product.stock <= 0:
        messages.error(request, f"{product.p_name} is out of stock.")
        return redirect('view_cart')
    image_obj = Product_image.objects.filter(p_id=product.p_id).first()
    try:
        discount = Discount.objects.get(product=product)
        price = discount.discounted_price
        disc_percent = discount.disc_percent
    except Discount.DoesNotExist:
        price = product.price
        disc_percent = Decimal(0)
    cart, __ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = Cart_items.objects.get_or_create(
        cart=cart,
        user=request.user,
        product=product,
        image = image_obj.image if image_obj else None,
        defaults={'price': price, 'quantity': 1, 'disc_percent': disc_percent, 'disc_price': price}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()


    return redirect('view_cart')

@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = Cart_items.objects.filter(cart=cart)

    if request.method == "POST":
        cart_item_id = request.POST.get("cart_item_id")
        action = request.POST.get("action")
        cart_item = get_object_or_404(Cart_items, id=cart_item_id, cart=cart)

        # Prevent increasing beyond stock
        if action == "increase" and cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        return redirect('view_cart')

    updated_cart = []
    total_mrp = Decimal(0)
    total_discount = Decimal(0)

    for item in cart_items:
        price = item.product.price
        try:
            discount = Discount.objects.get(product=item.product)
            disc_price = discount.discounted_price
            disc_percent = discount.disc_percent
        except Discount.DoesNotExist:
            disc_price = price
            disc_percent = Decimal(0)

        total_mrp += price * item.quantity
        total_discount += (price - disc_price) * item.quantity

        image_obj = Product_image.objects.filter(p_id=item.product).first()

        # Pass stock along with item
        item.price = price
        item.disc_price = disc_price
        item.disc_percent = disc_percent
        item.image = image_obj.image if image_obj else None
        item.stock = item.product.stock  # 👈 Add stock here

        updated_cart.append(item)

    discounted_total = total_mrp - total_discount

    if discounted_total > 50000:
        shipping = Decimal(250)
    elif discounted_total > 25000:
        shipping = Decimal(150)
    elif discounted_total > 5000:
        shipping = Decimal(100)
    else:
        shipping = Decimal(50)

    platform_fee = Decimal(10)
    final_total = discounted_total + shipping + platform_fee

    total_items = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0

    # Store totals in cart object
    cart.total_mrp = total_mrp
    cart.total_discount = total_discount
    cart.shipping = shipping
    cart.platform_fee = platform_fee
    cart.final_total = final_total
    cart.total_quantity = total_items
    cart.save()

    recommended_ids = weighted_hybrid_recommendations(request, top_k=6)
    recommended_products = Products.objects.filter(p_id__in=recommended_ids)

    context = {
        'cart_items': updated_cart,
        'total_items': total_items,
        'cart': cart,
        'recommended_products': recommended_products,
    }

    return render(request, 'user/cart/cart.html', context)


def delete_item(request,id):
    cart_items = Cart_items.objects.get(id=id,user=request.user)
    cart_items.delete()
    return redirect('view_cart')


@login_required
def toggle_wishlist(request, product_id):
    product = Products.objects.get(p_id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product)

    if wishlist_item.exists():
        wishlist_item.delete()
    else:
        Wishlist.objects.create(user=request.user, product=product)

    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    total_items = Decimal(0)
    for item in wishlist_items:
        product = item.product
        item.product_image = Product_image.objects.filter(p_id=item.product).first()
        try:
            discount = Discount.objects.get(product=product)
            item.disc_price = discount.discounted_price
            item.disc_percent = discount.disc_percent
        except Discount.DoesNotExist:
            item.disc_price = item.price
            item.disc_percent = Decimal(0)
    if wishlist_items:
        total_items = wishlist_items.count()
    return render(request, 'user/cart/wishlist.html', {'wishlist_items': wishlist_items,'total_items':total_items})

def delete_wishlist(request,id):
    wishlist_items = Wishlist.objects.get(id=id,user=request.user)
    wishlist_items.delete()
    return redirect('view_wishlist')

def add_address(request):
    address = Address.objects.all()
    if request.method =="POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        contact_no = request.POST.get('contact_no')
        address = Address.objects.create(user=request.user,name=name,address=address,pincode=pincode,contact_no=contact_no)
        next_url = request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('view_address')
        


def view_address(request):
    address= Address.objects.filter(user=request.user)
    default_address = Default_address.objects.filter(user=request.user).first()
    return render(request,'user/cart/address.html',locals())


def delete_address(request,id):
    address = Address.objects.get(id=id,user=request.user)
    address.delete()
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
       
    return redirect('view_address')

def update_address(request,id):
    address = Address.objects.get(id=id, user=request.user)
    if request.method == "POST":
        address.name = request.POST.get("name")
        address.address =request.POST.get("address")
        address.pincode = request.POST.get("pincode")
        address.contact_no = request.POST.get("contact_no")
        print(address.name,address.address)
        address.save()
        return redirect('view_address')
    return render(request,'user/cart/update_address.html',locals())

def mark_as_default(request, id):
    address = Address.objects.get(id=id, user=request.user)
    Default_address.objects.filter(user=request.user).delete()
    Default_address.objects.create(user=request.user, address=address)

    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('view_address') 

def delivery_details(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = Cart_items.objects.filter(cart=cart)
    default_address = Default_address.objects.filter(user=request.user).first()
    return render(request, "user/cart/delivery_details.html", locals())