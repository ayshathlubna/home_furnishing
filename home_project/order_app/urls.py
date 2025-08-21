# cart_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('placed_order/', views.placed_order, name="placed_order"),
    path('successful_order/',views.successful_order,name="successful_order"),
    path('orders/',views.orders,name="orders"),
    path('order_details/<str:id>/',views.order_details,name="order_details")
]
