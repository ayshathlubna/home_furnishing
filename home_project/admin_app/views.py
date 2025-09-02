from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from user_app.models import Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from product_app.models import Products
from category_app.models import Category
from sub_category_app.models import Sub_category
from order_app.models import Order,Order_items
from newsletter_app.models import NewsletterSubscriber
from django.http import HttpResponseForbidden
# Create your views here.

def admin_home(request):
    return render(request,"admin/admin_extend.html")

@login_required
def dashboard(request):

    section = request.GET.get('section', 'default')
    users = None
    staff = None
    products = None
    category = None
    sub_category = None
    orders = None
    subscribers = None
    selected_category = request.GET.get('category')

    categories = Category.objects.all()
    if section == 'user':
        users = User.objects.all()
    elif section == 'products':
        if selected_category:
            products = Products.objects.filter(category__category_id=selected_category)
        else:
            products = Products.objects.all()
    elif section == 'category':
        category = Category.objects.all()
    elif section == 'sub_category':
        sub_category = Sub_category.objects.all()
    elif section == 'orders':
        orders = Order.objects.all()
    elif section == 'requests':
        # All pending cancellation and return requests
        context['requests'] = Order_items.objects.filter(
            refund_status__in=['cancellation_requested', 'return_requested']
        ).order_by('-order__order_date')

    elif section == 'newsletter':
        subscribers = NewsletterSubscriber.objects.all()
        print("subscribers",subscribers)
    elif section == 'staff':
        staff = User.objects.filter(is_staff=True)

    context = {
        "section": section,
        "categories": categories,
        "sub_categories":sub_category,
        "users": users,
        "products": products,
        "orders": orders,
        "subscribers": subscribers,
        "staff": staff,
    }

    return render(request, 'admin/dashboard.html', context)



@login_required
@staff_member_required(login_url='signin')
def userlist(request):
    users = User.objects.all()
    return render(request,'admin/userlists.html',locals())

def new_staff(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Not authorized")

    gender_choices = Profile.gender_choice

    if request.method == "POST":
        first = request.POST.get("first_name")
        last = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        contact_no = request.POST.get("contact_no")
        address = request.POST.get("address")
        profile_pic = request.FILES.get("profile")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            user = User.objects.create_user(
                username=username,
                first_name=first,
                last_name=last,
                email=email,
                password=password,
                is_staff=True  # mark as staff
            )
            profile = Profile.objects.create(
                user=user,
                gender=gender,
                phone=contact_no,
                address=address,
                profile_img=profile_pic
            )
            messages.success(request, "Staff user created successfully")
            return redirect('dashboard')

    return render(request, 'admin/new_staff.html', {"gender": gender_choices})

@login_required
def staff_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Not authorized")
    
    # Get only users who are staff
    staff_users = User.objects.filter(is_staff=True).order_by('id')
  
    context = {
        "staff_users": staff_users
    }
    return render(request, 'admin/staff_list.html', context)


@login_required
def user_update(request,id):
    gender=Profile.gender_choice
    user=User.objects.get(id=id)
    profile=Profile.objects.get_or_create(user=user)

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
        return redirect('dashboard')
    
    return render(request,"admin/user_update.html",locals())
@login_required
def user_delete(request,id):
    user=User.objects.get(id=id)
    user.delete()
    return redirect('dashboard')

@login_required
def status_update(request,id):
    user = User.objects.get(id=id)
    if user.is_active:
        user.is_active=False
    else:
        user.is_active=True
    user.save()
    return redirect('dashboard')

@login_required
def staff_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Not authorized")
    
    # Get only users who are staff
    staff_users = User.objects.filter(is_staff=True).order_by('id')

    context = {
        "staff_users": staff_users
    }
    return render(request, 'admin/staff_list.html', context)
