from django.db import models
from category_app.models import Category
from sub_category_app.models import Sub_category
import datetime

# Create your models here.

class Products(models.Model):
    p_id = models.CharField(primary_key=True,max_length=20)
    date = models.DateField(default=datetime.date.today)
    p_name = models.CharField(max_length=100)
    color = models.CharField(max_length=20,blank=True,null=True)
    brand = models.CharField(max_length=20,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    description = models.CharField(max_length=20,blank=True)
    stock = models.IntegerField()
    price = models.DecimalField(decimal_places=2,max_digits=10)
    warranty = models.CharField(max_length=20,blank=True)

    def __str__(self):
        return self.p_name
    
class Product_image(models.Model):
    p_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_image/',null=True)

class Discount(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    disc_percent = models.FloatField(default=0)
    disc_price = models.DecimalField(max_digits=20,decimal_places=2, default=0)
    discounted_price = models.DecimalField(max_digits=20,decimal_places=2,default=0)

    