from django.contrib import admin
from order_app.models import Order,Order_items

# Register your models here.
admin.site.register(Order)
admin.site.register(Order_items)