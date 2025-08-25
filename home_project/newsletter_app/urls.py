from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.subscribe_newsletter_ajax, name='subscribe_newsletter'),
    path('newsletters/', views.newsletter_list, name='newsletter_list'),
]
