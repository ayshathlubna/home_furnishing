# cart_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add/<str:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('', views.view_cart, name='view_cart'),
    path("delete_item<int:id>/",views.delete_item,name="delete_item"),
    path('toggle_wishlist<str:product_id>/',views.toggle_wishlist,name="toggle_wishlist"),
    path('view_wishlist/',views.view_wishlist,name = "view_wishlist"),
    path("delete_wishlist<int:id>/",views.delete_wishlist,name="delete_wishlist"),
    path('add_address/',views.add_address,name="add_address"),
    path('view_address/',views.view_address,name="view_address"),
    path('delete_address/<int:id>/',views.delete_address,name='delete_address'),
    path('update_address/<int:id>/',views.update_address,name="update_address"),
    path('mark_as_default/<int:id>/', views.mark_as_default, name='mark_as_default'),
    path('delivery_details/',views.delivery_details,name="delivery_details")

]
