from django.contrib import admin
from order_app.models import Order_items,Order

# Register your models here.
admin.site.register(Order)
admin.site.register(Order_items)