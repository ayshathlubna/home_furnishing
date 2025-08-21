from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from product_app.models import Products

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_quantity = models.IntegerField(default=0)
    total_mrp = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    total_discount = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    shipping = models.IntegerField(default=0)
    platform_fee = models.IntegerField(default=0)
    final_total = models.DecimalField(default=0,max_digits=10, decimal_places=2)
class Cart_items(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.PositiveIntegerField(default=1)
    disc_percent = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    disc_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    image = models.ImageField(upload_to='product_image/',null=True)
    added_on = models.DateTimeField(auto_now_add=True)


    def item_total(self):
        return self.price * self.quantity
    

    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10,default=0)
    disc_percent = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    disc_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    image = models.ImageField(upload_to='product_image/',null=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.p_name}"

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length=500)
    pincode = models.IntegerField()
    contact_no = models.IntegerField()
    
class Default_address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.OneToOneField(Address,on_delete=models.CASCADE)
