from django.urls import path
from . import views

urlpatterns = [
    path('add_sub_category/',views.add_sub_category,name='add_sub_category'),
    path('',views.display_sub_category, name='display_sub_category'),
    path('update_sub_category/<str:id>/',views.update_sub_category,name='update_sub_category'),
    path('delete_sub_category/<str:id>/',views.delete_sub_category,name='delete_sub_category')

]
