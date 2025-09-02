
from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('userlist/', views.userlist,name="userlist"),
    path('new_staff/',views.new_staff,name="new_staff"),
    path('user_update/<int:id>',views.user_update,name='user_update'),
    path('user_delete/<int:id>',views.user_delete,name='user_delete'),
    path('status_update/<int:id>',views.status_update,name='status_update'),
    path('staff_list/', views.staff_list, name='staff_list'),
 ]
