
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path("brands/<str:brand>/", views.product_page, name="brand_products"),

    path('aboutus/',views.aboutus,name='aboutus'),
    path('living/<str:id>',views.living,name='living'),
    path('bedroom/<str:id>',views.bedroom,name='bedroom'),
    path('dining/<str:id>',views.dining,name='dining'),
    path('decor/<str:id>',views.decor,name='decor'),
    path('kids/<str:id>',views.kids,name='kids'),
    path('lighting/<str:id>',views.lighting,name='lighting'),
    path('kitchen/<str:id>',views.kitchen,name='kitchen'),
    path('product_page/', views.product_page, name='product_page'),
    path('product_page/<str:id>',views.product_page,name='product_page'),
    path('products/<str:id>/<str:sub_id>/', views.product_page, name='product_page'),
    path('signup/', views.signup,name="signup"),
    path('signin/',views.signin,name="signin"),
    path('profile/',views.profile , name='profile'),
    path('profile_update/', views.profile_update, name="profile_update"),
    path('delete-profile/', views.profile_delete, name='profile_delete'),
    path('logout/',views.logout_profile,name='logout'),
    path('search_page/',views.search_page,name="search_page")
    # path('sort/',views.sort,name='sort')
]


