from django.shortcuts import render,redirect
from category_app.models import Category
from sub_category_app.models import Sub_category
from product_app.models import Products,Product_image,Discount
from itertools import zip_longest
from django.db.models import Case, When
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from cart_app.models import Cart_items,Wishlist
from django.db.models import Sum

# Create your views here.
def home(request):
    user = User.objects.all()
    if request.user.is_authenticated:
        total_items = Cart_items.objects.filter(cart__user=request.user).aggregate(Sum('quantity'))['quantity__sum'] or 0
    return render(request,'user/home.html',locals())

def group_items(lst, group_size):
    lst = list(lst)  # Convert QuerySet to list
    extended = lst + lst[:group_size * 2]
    return [extended[i:i + group_size] for i in range(0, len(lst), group_size)]

def living(request,id):
    category = Category.objects.get(category_id=id)
    sub_category = Sub_category.objects.filter(category=category)
    all_products = Products.objects.filter(sub_category__in=sub_category)
    product_images = []

    exclusive_products = [
    
    "Abby Fabric 3-Seater Sofa with Cushions",
    "Giza Composite Marble Top Coffee Table ",
    "Homeshores TV Unit",
    "Modern Radiance TV Unit",
    "Helios Bill Coffee Table",
    "Helios Emily Fabric 3+2+1 Seater Sofa Set"
    ]

    filtered_products = all_products.filter(p_name__in=exclusive_products)

    for i in filtered_products:
        image = Product_image.objects.filter(p_id=i).first()
        if image:
            product_images.append({'product': i, 'image': image.image})

    product_groups = group_items(product_images, 4)
    return render(request,'user/living.html',locals())

def bedroom(request,id):
    category = Category.objects.get(category_id=id)
    sub_category = Sub_category.objects.filter(category=category)
    all_products = Products.objects.filter(sub_category__in=sub_category)
    product_images = []

    exclusive_products = [
    
    "Helios Alton 4-Door Wardrobe with Mirrors",
    "Lexus Savanna King Bed with Hydraulic Storage",
    "Saga Bedside Table with Drawers",
    "Tiffany Caramel Queen Bed with Hydraulic Storage ",
    "Senorita 4-Door Wardrobe with Mirrors",
    "Vegas Bed Side Table with Drawers"
    ]

    filtered_products = all_products.filter(p_name__in=exclusive_products)

    for i in filtered_products:
        image = Product_image.objects.filter(p_id=i).first()
        if image:
            product_images.append({'product': i, 'image': image.image})

    product_groups = group_items(product_images, 4)
    return render(request,'user/bedroom.html',locals())

def dining(request,id):
    category = Category.objects.get(category_id=id)
    sub_category = Sub_category.objects.filter(category=category)
    all_products = Products.objects.filter(sub_category__in=sub_category)
    product_images = []

    exclusive_products = [
    
    "Vegas Faux Marble Top 6-Seater Dining Set with Chairs",
    "Harmony Sia Set of 2 Faux Leather Dining Chairs",
    "Helios Reynan NXT Crockery Unit",
    "Modern Radiance Set of 2 Fabric Dining Chairs",
    "Hadley Buffet Sideboard",
    "Montoya 4-Seater Dining Set with Chairs and Bench"
    ]

    filtered_products = all_products.filter(p_name__in=exclusive_products)

    for i in filtered_products:
        image = Product_image.objects.filter(p_id=i).first()
        if image:
            product_images.append({'product': i, 'image': image.image})

    product_groups = group_items(product_images, 4)
    return render(request,'user/dining.html',locals())

def decor(request,id):
    category = Category.objects.get(category_id=id)
    sub_category = Sub_category.objects.filter(category=category)
    all_products = Products.objects.filter(sub_category__in=sub_category)
    product_images = []

    exclusive_products = [
    
    "Sierra Set of 2 Woven Room Darkening Door Curtains - 7ft",
    "Corsica Esteem Classic Woven Carpet - 183x122cm",
    "Iliano Metal Flowers and Leaves Wall Accent",
    "Contempo Set of 2 Colourblocked Room Darkening Door Curtains - 7ft",
    "Paradis Rafael Nylon Woven Carpet - 180x120cm",
    "Corvus Mystic Polypropylene Set of 3 Decorative Wall Arts"
    ]

    filtered_products = all_products.filter(p_name__in=exclusive_products)

    for i in filtered_products:
        image = Product_image.objects.filter(p_id=i).first()
        if image:
            product_images.append({'product': i, 'image': image.image})

    product_groups = group_items(product_images, 4)
    return render(request,'user/decor.html',locals())

def kids(request,id):
    category = Category.objects.get(category_id=id)
    sub_category = Sub_category.objects.filter(category=category)
    all_products = Products.objects.filter(sub_category__in=sub_category)
    product_images = []

    exclusive_products = [
    
    "Capel Kids Trundle Bed with Headboard Storage | (78x36 inch)",
    "Slate Kids Penguin Filled Cushion - 30x40cm",
    "Back To School Spark Set of 2 Stainless Steel Insulated Lunch Box",
    "Sunbeam Kids Bed | (72x36 inch) | (White & Yellow)",
    "Slate Kids Unicorn Filled Cushion",
    "Korobka Taze Set of 3 Stainless Steel Lunch Boxes with Bag"
    ]

    filtered_products = all_products.filter(p_name__in=exclusive_products)

    for i in filtered_products:
        image = Product_image.objects.filter(p_id=i).first()
        if image:
            product_images.append({'product': i, 'image': image.image})

    product_groups = group_items(product_images, 4)
    return render(request,'user/kids.html',locals())

def lighting(request,id):
    category = Category.objects.get(category_id=id)
    sub_category = Sub_category.objects.filter(category=category)
    all_products = Products.objects.filter(sub_category__in=sub_category)
    product_images = []

    exclusive_products = [
    
    "Melody Shellacs Glass Pendant Lamp",
    "HOMESAKE Metal Floor Lamp",
    "Riviera Dune Ceramic Table Lamp",
    "HOMESAKE Metal Pendant Ceiling Lamp",
    "Fluorescence Glint Metal Floor Lamp with Shelves	",
    "Monolith Marvel Ceramic Pebble Table Lamp"
    ]

    filtered_products = all_products.filter(p_name__in=exclusive_products)

    for i in filtered_products:
        image = Product_image.objects.filter(p_id=i).first()
        if image:
            product_images.append({'product': i, 'image': image.image})

    product_groups = group_items(product_images, 4)
    return render(request,'user/lighting.html',locals())

def kitchen(request,id):
    category = Category.objects.get(category_id=id)
    sub_category = Sub_category.objects.filter(category=category)
    all_products = Products.objects.filter(sub_category__in=sub_category)
    product_images = []

    exclusive_products = [
    "Gravis Stellar 5Pcs Triply Stainless Steel Cookware Set",
    "Spinel Bamboo Chopping Board",
    "Corsica Set of 3 Polypropylene Storage Containers - 450ml",
    "Valeria Carin Triply Stainless Steel Pressure Cooker - 3L",
    "Jarvis Hobbiton Set of 3 Stainless Steel Kitchen Scissors",
    "Mendo Dolomite Cookie Jar - 1.48L"
    ]

    filtered_products = all_products.filter(p_name__in=exclusive_products)

    for i in filtered_products:
        image = Product_image.objects.filter(p_id=i).first()
        if image:
            product_images.append({'product': i, 'image': image.image})

    product_groups = group_items(product_images, 4)
    return render(request,'user/kitchen.html',locals())

def group_sub_items(items, group_size):
    items = list(items)
    if not items:
        return []

    num_groups = (len(items) + group_size - 1) // group_size

    # Extend list to make total items = num_groups * group_size
    extended_items = items.copy()
    while len(extended_items) < num_groups * group_size:
        extended_items += items  # Repeat if needed

    extended_items = extended_items[:num_groups * group_size]

    # Split into chunks of group_size
    return [extended_items[i:i + group_size] for i in range(0, len(extended_items), group_size)]

# def product_page(request,id=None,sub_id=None):
    
#     category = Category.objects.all()
#     sub_cats = Sub_category.objects.all()
#     selected_category=request.GET.get('category') 
#     print("aaa",selected_category)
  
#     order =request.GET.get('order') 

#     if selected_category:
#         sub_categories = Sub_category.objects.filter(category_id=selected_category)
#         all_products = Products.objects.filter(sub_category__in=sub_categories)
        
#     else:
#         sub_categories = Sub_category.objects.all()
#         all_products = Products.objects.all()


#     product_images = []
#     if sub_id:
#         all_products=Products.objects.filter(sub_category=sub_id)
       
#         # print(all_products)

#     if order == 'asc':
#         all_products = all_products.order_by('date')
#     elif order == 'desc':
#         all_products = all_products.order_by('-date')
#     elif order == 'lowest':
#         all_products = all_products.order_by('price')
#     elif order == 'highest':
#         all_products = all_products.order_by('-price')
#     elif order == 'high_disc':
#         discounted = Discount.objects.all().order_by('-disc_percent')
#         product_ids = [disc.product.id for disc in discounted]
#         preserved = Case(*[When(id=pid, then=pos) for pos, pid in enumerate(product_ids)])
#         all_products = Products.objects.filter(id__in=product_ids).order_by(preserved)

from django.db.models import Case, When

def product_page(request, id=None, sub_id=None):
    category = Category.objects.all()
    sub_cats = Sub_category.objects.all()
    wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)

    selected_category = request.GET.get('category')
    
    order = request.GET.get('order')
    
    all_products = Products.objects.all()
    
    category_name = None
    subcategory_name = None


    # 1. If subcategory is selected from carousel/navbar
    if sub_id and sub_id != 'None':
        all_products = Products.objects.filter(sub_category=sub_id)
        try:
            sub_obj = Sub_category.objects.get(sub_cat_id=sub_id)
            selected_category = sub_obj.category.category_id  # for keeping the filter selected
            category_name = sub_obj.category.category_name
            subcategory_name = sub_obj.sub_cat_name
        except Sub_category.DoesNotExist:
            pass

    # 2. If category is selected from dropdown
    elif selected_category:
        print('fgfg')
        sub_categories = Sub_category.objects.filter(category_id=selected_category)
        print(sub_categories)
        all_products = Products.objects.filter(sub_category__in=sub_categories)
        print(all_products)
        category_name = Category.objects.get(category_id=selected_category).category_name

    # 3. Sorting logic
    if order == 'asc':
        all_products = all_products.order_by('date')
    elif order == 'desc':
        all_products = all_products.order_by('-date')
    elif order == 'lowest':
        all_products = all_products.order_by('price')
    elif order == 'highest':
        all_products = all_products.order_by('-price')
    elif order == 'high_disc':
        discounts = Discount.objects.filter(product__in=all_products).order_by('-disc_percent')
        discounted_ids = [disc.product.p_id for disc in discounts]
        rank_map = {pid: pos for pos, pid in enumerate(discounted_ids)}
        preserved = Case(*[
            When(p_id=pid, then=rank_map.get(pid, 9999))
            for pid in all_products.values_list('p_id', flat=True)
        ])
        all_products = all_products.order_by(preserved)

    product_images = []
    for product in all_products:
        image = Product_image.objects.filter(p_id=product).first()
        discount = Discount.objects.filter(product=product).first()
        print(discount)
        product_images.append({
            'product_id': product,
            'image': image,
            'discount': discount
        })

    sub_cat_groups = group_items(sub_cats, 6)

    return render(request, 'user/product_page.html', locals())

def signup(request):
    if request.method== "POST":
        first = request.POST.get("first")
        last = request.POST.get("last")
        username = request.POST.get("username")
        print(username)
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        email = request.POST.get("email")
        users=User.objects.filter(username=username).values()
        print(users)
        if users:
            messages.error(request,"Username already exists")
            return redirect("signup")
        if confirm_password==password:
            user = User.objects.create(first_name = first, last_name=last, username = username,email=email)
            user.set_password(password)
            user.save()
            # Profile.objects.create(user=user)
            return redirect('signin')
        else:
            messages.error(request,"Password doesn't match")
    return render(request,"user/signuppage.html")

@never_cache
def signin(request):
     
    if request.method =="POST":
        username=request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        user = authenticate(username = username, password=password)
        print(user)
        if user:
            # print(user)
            # if user.is_superuser:
            #     login(request,user)
            #     return redirect('userlist')
            # else:
                login(request,user)
                return redirect('home')
        else:
          messages.error(request, "User not found or password is incorrect.")
    return render(request,"user/loginpage.html")


@login_required    
@never_cache
def profile(request):
    return render(request,"user/profile.html")

# def get_profile(request, ):
#     profile = User.objects.get(id=id)
#     return render(request,"update_profile.html",locals())

@login_required 
def profile_update(request):
    gender=Profile.gender_choice
    user=request.user
    profile=Profile.objects.get_or_create(user=user)
    print(user,profile)

    if request.method=="POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        # userusername = request.POST.get("username")
        user.email = request.POST.get("email")
        user.profile.gender = request.POST.get("gender")
        user.profile.mobile = request.POST.get("contact_no")
        user.profile.address = request.POST.get("address")
        img=request.FILES.get('profile')
        print(img)
        print(user.first_name,user.last_name, user.profile.mobile)
        if img:
            user.profile.profile_img=img

        user.save()

        user.profile.save()
        return redirect('profile')
    
    return render(request,"user/profile_update.html",locals())

def profile_delete(request):
    user = request.user
    user.delete()
    return redirect('signin')

@never_cache
def logout_profile(request):
    logout(request)
    return redirect('home')

