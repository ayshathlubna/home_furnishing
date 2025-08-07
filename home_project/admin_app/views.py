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
# Create your views here.

def admin_home(request):
    return render(request,"admin/admin_extend.html")

@login_required
def dashboard(request):

    section = request.GET.get('section', 'default')
    selected_category = request.GET.get('category')
    if section == 'user':
        users = User.objects.all()
    else:
        users = None

    categories = Category.objects.all()
    if section == "products":
        if selected_category:
            products = Products.objects.filter(category__category_id=selected_category)
        else:
            products = Products.objects.all()


    return render(request, 'admin/dashboard.html', locals())



@login_required
@staff_member_required(login_url='signin')
def userlist(request):
    users = User.objects.all()
    return render(request,'admin/userlists.html',locals())

@login_required
def new_user(request):
    gender=Profile.gender_choice
    if request.method =="POST":
        first = request.POST.get("first_name")
        last = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        contact_no = request.POST.get("contact_no")
        address = request.POST.get("address")

        users=User.objects.filter(username=username).values()
        if users:
            messages.error(request,"Username already exists")
        
        if confirm_password==password:
            user = User.objects.create(first_name = first, last_name=last, username = username,email=email)
            user.set_password(password)
            profile =Profile.objects.create(user=user,gender=gender, mobile=contact_no,address=address)
            user.save()
            profile.save()
            return redirect('admin_page')
    return render(request,'admin/new_user.html',locals())

# def getuser(request,id):
#     user = User.objects.get(id=id)
#     return redirect('user_update',user.id)
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
        return redirect('admin_page')
    
    return render(request,"admin/user_update.html",locals())
@login_required
def user_delete(request,id):
    user=User.objects.get(id=id)
    user.delete()
    return redirect('admin_page')

@login_required
def status_update(request,id):
    user = User.objects.get(id=id)
    if user.is_active:
        user.is_active=False
    else:
        user.is_active=True
    user.save()
    return redirect('admin_page')

