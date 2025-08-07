from django.urls import path
from . import views

urlpatterns = [
    path('add_category/',views.Add_category,name='add_category'),
    path('',views.display_category, name='display_category'),
    path('update_category/<str:id>/', views.update_category, name='update_category'),
    path('delete_category/<str:id>/', views.delete_category, name='delete_category'),
]
