from django.urls import path
from . import views

urlpatterns = [
    path('add_product/',views.add_product,name='add_product'),
    path('',views.display_product,name='display_product'),
    path('get_subcategories/<str:category_id>/', views.get_subcategories, name='get_subcategories'),
    path('delete_product/<str:id>',views.delete_product,name='delete_product'),
    path('update_product/<str:id>',views.update_product,name='update_product'),
    path('discount/',views.discount,name='discount'),
    path('delete_discount/<str:id>', views.delete_discount, name='delete_discount'),
    path('update_discount/<str:id>', views.update_discount, name='update_discount'),
    path('product_details/<str:id>',views.product_details,name="product_details")

]
