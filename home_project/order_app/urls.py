# cart_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('placed_order/', views.placed_order, name="placed_order"),
    path('successful_order/',views.successful_order,name="successful_order"),
    path('orders/',views.orders,name="orders"),
    path('order_details/<str:id>/',views.order_details,name="order_details"),
    path("cancel_order/<int:item_id>/", views.cancel_order, name="cancel_order"),
    path('request_return/<int:item_id>/', views.request_return, name='request_return'),
]
