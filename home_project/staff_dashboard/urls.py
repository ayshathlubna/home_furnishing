from django.urls import path
from . import views

urlpatterns = [
    path('order_list/', views.order_list, name='staff_order_list'),
    path('staff_order_detail/<str:order_id>/', views.staff_order_detail, name='staff_order_detail'),
]