from django.db import models
from django.contrib.auth.models import User
from cart_app.models import Address
from product_app.models import Products

# Create your models here.
import uuid

class Order(models.Model):
    order_id = models.CharField(primary_key=True, max_length=50, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_quantity = models.IntegerField(default=0)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_savings = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    payment_choices = [
        ('Cash on Delivery', 'Cash on Delivery'),
        ('NetBanking', 'NetBanking'),
        ('UPI Payment', 'UPI Payment'),
        ('Wallet','Wallet')
    ]
    payment_method = models.CharField(max_length=30, choices=payment_choices)

    payment_status_choices = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Refunded', 'Refunded')
    ]
    payment_status = models.CharField(max_length=20, choices=payment_status_choices,default='Pending')

    status_choices = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Refunded','Refunded'),
        ('Partially Refunded','Partially Refunded')
    ]
    delivery_status = models.CharField(max_length=25, choices=status_choices, default='pending')
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField(null=True, blank=True)
    refund_status_choices = [
        ('Not Requested', 'Not Requested'),
        ('Requested', 'Requested'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]
    refund_status = models.CharField(max_length=20, choices=refund_status_choices, default='Not Requested')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.order_id)


class Order_items(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField(null=True)
    quantity = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status_choices = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Refunded','Refunded'),
        ('Partially Refunded','Partially Refunded')
    ]
    delivery_status = models.CharField(max_length=25, choices=status_choices, default='pending')
    refund_status_choices = [
        ('Not Requested', 'Not Requested'),
        ('Requested', 'Requested'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]
    refund_status = models.CharField(max_length=20, choices=refund_status_choices, default='Not Requested')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.product} x {self.quantity}"
