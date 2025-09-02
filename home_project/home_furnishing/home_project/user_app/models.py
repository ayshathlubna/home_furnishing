from django.db import models
from django.contrib.auth.models import User
from product_app.models import Products

# Create your models here.
class Profile(models.Model):
    gender_choice = [('male','male'), ('female','female')]
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(choices=gender_choice, max_length=20)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_img = models.ImageField(upload_to='profile_picture/', null=True)


class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-viewed_at"]  # latest first


