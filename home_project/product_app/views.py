from django.shortcuts import render,redirect
from category_app.models import Category
from sub_category_app.models import Sub_category
from .models import Products, Product_image, Discount
from django.contrib import messages
from cart_app.models import Wishlist

# Create your views here.
def add_product(request):
    categories = Category.objects.all()
    sub_categories = Sub_category.objects.all()
    if request.method == "POST":
        p_id = request.POST.get("p_id")
        p_name = request.POST.get("p_name")
        color = request.POST.get('color')
        brand = request.POST.get('brand')
        category = request.POST.get('category')

        sub_cat_id = request.POST.get('sub_category')
        check_sub_cat = Sub_category.objects.get(sub_cat_id=sub_cat_id)

        description = request.POST.get('description')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        warranty = request.POST.get('warranty')
        images = request.FILES.getlist('images')
       
        check_cat = Category.objects.get(category_id=category)
        check_pid = Products.objects.filter(p_id=p_id)
        if check_pid:
            messages.error(request,"Product ID already exists")
            return redirect('add_product')
        else:
            product=Products.objects.create(p_id = p_id , p_name=p_name, color=color, brand=brand, category = check_cat, sub_category=check_sub_cat, description=description,stock=stock, price=price,warranty=warranty)
            for i in images:
                Product_image.objects.create(p_id = product, image=i)
 
            return redirect('display_product')      
    return render(request, 'admin/product/insert_product.html',locals())

# def display_product(request):
#     products = Products.objects.all()
#     return render(request,"admin/product/display_product.html",locals())

def display_product(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    if selected_category:
        products = Products.objects.filter(category__category_id=selected_category)
    else:
        products = Products.objects.all()
    return render(request, "admin/product/display_product.html", {
        "products": products,
        "categories": categories,
        "selected_category": selected_category
    })



def update_product(request, id):
    products = Products.objects.get(p_id=id)
    product_image = Product_image.objects.filter(p_id=products).first()
    categories = Category.objects.all()

    if request.method == "POST":
        products.p_id = request.POST.get("p_id")
        products.date = request.POST.get("date")
        products.p_name = request.POST.get("p_name")
        products.color = request.POST.get("color")
        products.brand = request.POST.get("brand")
        products.description = request.POST.get("description")
        products.stock = request.POST.get("stock")
        products.price = request.POST.get("price")
        products.warranty = request.POST.get("warranty")

        # Update category
        selected_category_id = request.POST.get("category")
        if selected_category_id:
            try:
                category_obj = Category.objects.get(category_id=selected_category_id)
                products.category = category_obj
            except Category.DoesNotExist:
                print("Category not found!")

        # Update sub-category
        selected_sub_category_id = request.POST.get("sub_category")
        if selected_sub_category_id:
            try:
                sub_category_obj = Sub_category.objects.get(sub_cat_id=selected_sub_category_id)
                products.sub_category = sub_category_obj
            except Sub_category.DoesNotExist:
                print("Sub-category not found!")

        # Save product
        products.save()

        # Handle image upload
        images = request.FILES.getlist("images")
        if images:
            Product_image.objects.filter(p_id=products).delete()  # optional
            for image in images:
                Product_image.objects.create(p_id=products, image=image)


        return redirect('display_product')

    return render(request, 'admin/product/update_product.html', locals())


def delete_product(request,id):
    products = Products.objects.get(p_id=id)
    products.delete()
    return redirect('display_product')

from django.http import JsonResponse
from .models import Sub_category, Category

def get_subcategories(request, category_id):
    print(category_id)
    sub_cats = Sub_category.objects.filter(category_id=category_id)
    print(sub_cats)
    data = {
        'sub_categories': [
            {'id': sub.sub_cat_id, 'name': sub.sub_cat_name}
            for sub in sub_cats
        ]
    }
    return JsonResponse(data)

from decimal import Decimal
def discount(request):
    products = Products.objects.all()
    discount = Discount.objects.all()
    show_modal = False
    if request.method == "POST":
        selected_p_id = request.POST.get('p_id')
        disc_percent = request.POST.get('disc_percent')    
        check_pid = Discount.objects.filter(product=selected_p_id)

        if check_pid :
            messages.error(request,"Discount already added to the product")
            show_modal = True
        else:
            p_id = Products.objects.get(p_id = selected_p_id)
            price = p_id.price
            disc_price = (price * Decimal(disc_percent)/100)
            discounted_price = (price - disc_price)
            Discount.objects.create(product = p_id, disc_percent=disc_percent, disc_price=disc_price,discounted_price=discounted_price)
            return redirect("discount")
        
    return render(request,"admin/product/discount.html",locals())

def update_discount(request,id):
    discount = Discount.objects.get(id=id)
    products = Products.objects.all()
    
    if request.method == "POST":   
        selected_pid= request.POST.get("p_id")
        discount.disc_percent = request.POST.get("disc_percent")

        check_pid = Discount.objects.filter(product=selected_pid)
        if check_pid :
            messages.error(request,"Product with discount already exist")
            show_modal = True
        else:
            product = Products.objects.get(p_id=selected_pid)
            discount.product = product 
            discount.disc_price = (product.price * Decimal(discount.disc_percent)/100)
            discount.discounted_price = (product.price - discount.disc_price)
            
            discount.save()
            return redirect('discount')
    
    return render(request, 'admin/product/update_discount.html', locals())


def delete_discount(request,id):
    discounts = Discount.objects.get(id=id)
    discounts.delete()
    return redirect('discount')

def product_details(request,id):
    product = Products.objects.get(p_id = id)
    product_image =Product_image.objects.filter(p_id=product)
    wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    discount = Discount.objects.filter(product=product).first()
    product_images = []
    all_products = Products.objects.filter(sub_category = product.sub_category).exclude(p_id=product.p_id)[:4]
    for p in all_products:
        image = Product_image.objects.filter(p_id=p).first()
        discount = Discount.objects.filter(product=p).first()
         # maintain session history
        
        product_images.append({
            'product_id': p,
            'image': image,
            'discount': discount
        })

        # Store recently viewed products in session
    recently_viewed = request.session.get('recently_viewed', [])
    
    if product.p_id not in recently_viewed:
        recently_viewed.insert(0, product.p_id)  # add to the front
        if len(recently_viewed) > 6:  # limit to last 6 products
            recently_viewed.pop()
    
    request.session['recently_viewed'] = recently_viewed
    print(" request.session['recently_viewed']", request.session['recently_viewed'])

    return render(request,'user/product_details.html',locals())

