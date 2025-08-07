from django.shortcuts import render,redirect
from category_app.models import Category
from .models import Sub_category
from product_app.models import Products
# Create your views here.

def add_sub_category(request):
    if request.method == "POST":
        sub_cat_id = request.POST.get("sub_cat_id")
        sub_cat_name = request.POST.get("sub_cat_name")
        category = request.POST.get("category")
        sub_cat_image = request.FILES.get("sub_cat_image")

        check_cat = Category.objects.get(category_name=category)
        Sub_category.objects.create(sub_cat_id=sub_cat_id,sub_cat_name=sub_cat_name,category=check_cat, sub_cat_image=sub_cat_image)
        return redirect('display_sub_category')

def display_sub_category(request):
    categories = Category.objects.all()
    sub_categories = Sub_category.objects.all()
    return render(request,"admin/sub_category/display_subcategory.html",locals())

def update_sub_category(request,id):
    sub_categories = Sub_category.objects.get(sub_cat_id=id)
    categories = Category.objects.all()
    
    if request.method == "POST":   
        sub_categories.sub_cat_id = request.POST.get("sub_cat_id")
        sub_categories.sub_cat_name = request.POST.get("sub_cat_name")
        sub_cat_image = request.FILES.get("sub_cat_image")
        if sub_cat_image:
            sub_categories.sub_cat_image = sub_cat_image
        selected_category_name = request.POST.get("category")
        category_obj = Category.objects.get(category_name=selected_category_name)
        sub_categories.category = category_obj 
        
        sub_categories.save()
        return redirect('display_sub_category')
    return render(request,'admin/sub_category/update_subcategory.html',locals())

def delete_sub_category(request,id):
    sub_categories = Sub_category.objects.get(sub_cat_id=id)
    sub_categories.delete()
    return redirect('display_sub_category')

def products(request,sub_id):
    products=Products.objects.filter(sub_category = sub_id)
    return 
