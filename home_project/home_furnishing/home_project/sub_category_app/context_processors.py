from sub_category_app.models import Sub_category

def all_subcategories(request):
    return {
        'all_subcategories': Sub_category.objects.all()
        
    }