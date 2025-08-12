from django.contrib import admin
from .models import Cart,Wishlist,Cart_items,Address,Default_address

admin.site.register(Cart)
admin.site.register(Cart_items)
admin.site.register(Wishlist)
admin.site.register(Address)
admin.site.register(Default_address)