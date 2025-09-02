from django.shortcuts import render,redirect
from .models import Category

# Create your views here.
def Add_category(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        category_name = request.POST.get("category_name")
        category_image = request.FILES.get('image')
        Category.objects.create(category_id=category_id,category_name=category_name,category_image=category_image)
        return redirect('display_category')

def display_category(request):
    categories = Category.objects.all()
    
    return render(request,"admin/category/display_category.html",locals())

        
def update_category(request, id):
    categorys = Category.objects.get(category_id=id)
    if request.method == "POST":   
        categorys.category_id = request.POST.get("category_id")
        categorys.category_name = request.POST.get("category_name")
        categorys.category_image = request.FILES.get("category_image")
        print(categorys.category_image)
        categorys.save()
        return redirect('display_category')
    return render(request,'admin/category/update_category.html',locals())

def delete_category(request, id):
    categories = Category.objects.get(category_id=id)
    categories.delete()
    return redirect('display_category')