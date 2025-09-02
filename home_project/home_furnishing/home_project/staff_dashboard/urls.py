from django.urls import path
from . import views

urlpatterns = [
    # Staff Order List & Detail
    path('order_list/', views.order_list, name='staff_order_list'),
    path('orders/<str:order_id>/', views.staff_order_detail, name='staff_order_detail'),
    path('',views.staff_dashboard,name="staff_dashboard"),

    # Approve / Reject Cancel or Return Requests
    path('approve/<int:item_id>/', views.approve_request, name='approve_request'),
    path('reject/<int:item_id>/', views.reject_request, name='reject_request'),

    # path('cancellation_requests/', views.cancellation_requests, name='cancellation_requests'),
    # path('return_requests/', views.return_requests, name='return_requests'),

    path('requests/', views.requests_dashboard, name='requests_dashboard'),
]
