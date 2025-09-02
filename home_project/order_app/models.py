from django.db import models
from django.contrib.auth.models import User
from product_app.models import Products
from datetime import timedelta
from django.utils import timezone
import uuid

class Order(models.Model):
    order_id = models.CharField(
        primary_key=True, max_length=50, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey('cart_app.Address', on_delete=models.CASCADE)
    total_quantity = models.IntegerField(default=0)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_savings = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    PAYMENT_METHOD_CHOICES = [
        ('Cash on Delivery', 'Cash on Delivery'),
        ('NetBanking', 'NetBanking'),
        ('UPI Payment', 'UPI Payment'),
        ('Wallet','Wallet')
    ]
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES)

    PAYMENT_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Refund Requested', 'Refund Requested'),
        ('Partially Refunded', 'Partially Refunded'),
        ('Refunded', 'Refunded'),
        ('Cancelled', 'Cancelled'), # For COD orders
    ]
    payment_status = models.CharField(max_length=25, choices=PAYMENT_STATUS_CHOICES, default='Pending')

    DELIVERY_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Cancellation Requested', 'Cancellation Requested'),
        ('Return Requested', 'Return Requested'),
        ('Returned','Returned'),
    ]
    delivery_status = models.CharField(max_length=25, choices=DELIVERY_STATUS_CHOICES, default='Pending')

    REFUND_STATUS_CHOICES = [
        ('Not Requested', 'Not Requested'),
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    refund_status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='Not Requested')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    order_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.order_id)

    # 🟢 Update order-level status based on its items
    def update_status_from_items(self):
        items = self.items.all()
        # Check if all items are cancelled or returned
        all_cancelled = all(item.delivery_status == 'Cancelled' for item in items)
        all_returned = all(item.delivery_status == 'Returned' for item in items)
        
        # Update delivery status
        if all_cancelled:
            self.delivery_status = 'Cancelled'
        elif all_returned:
            self.delivery_status = 'Returned'
        elif any(item.delivery_status == 'Return Requested' for item in items):
            self.delivery_status = 'Return Requested'
        elif any(item.delivery_status == 'Cancellation Requested' for item in items):
            self.delivery_status = 'Cancellation Requested'
        elif all(item.delivery_status == 'Delivered' for item in items):
            self.delivery_status = 'Delivered'
        elif any(item.delivery_status == 'Shipped' for item in items):
            self.delivery_status = 'Shipped'
        else:
            self.delivery_status = 'Pending'

        # Update payment status
        items_refunded = items.filter(refund_status='Completed').count()
        total_items = items.count()
        if items_refunded == total_items:
            self.payment_status = 'Refunded'
        elif items_refunded > 0:
            self.payment_status = 'Partially Refunded'
        elif any(item.payment_status == 'Refund Requested' for item in items):
            self.payment_status = 'Refund Requested'
        else:
            # Revert to 'Paid' for online orders or 'Pending' for COD
            if self.payment_method != 'Cash on Delivery':
                self.payment_status = 'Paid'
            else:
                self.payment_status = 'Pending'

        # Update refund status
        if items_refunded == total_items:
            self.refund_status = 'Completed'
        elif items_refunded > 0:
            self.refund_status = 'Pending'
        else:
            self.refund_status = 'Not Requested'
        
        self.save()


class Order_items(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.ImageField(null=True)
    quantity = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_date = models.DateField(null=True, blank=True)

    DELIVERY_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Cancellation Requested', 'Cancellation Requested'),
        ('Returned', 'Returned'),
        ('Return Requested', 'Return Requested'),
    ]
    delivery_status = models.CharField(max_length=25, choices=DELIVERY_STATUS_CHOICES, default='Pending')

    PAYMENT_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Refund Requested', 'Refund Requested'),
        ('Refunded', 'Refunded'),
        ('Cancelled', 'Cancelled'),
    ]
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')

    REFUND_STATUS_CHOICES = [
        ('Not Requested', 'Not Requested'),
        ('Requested', 'Requested'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]
    refund_status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='Not Requested')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def can_return(self):
        """Allows return if delivered and within 7 days."""
        if self.delivery_status == "Delivered" and self.delivery_date:
            return timezone.now().date() <= (self.delivery_date + timedelta(days=7))
        return False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the parent order's status whenever an item is changed
        self.order.update_status_from_items()

    def __str__(self):
        return f"{self.product} x {self.quantity}"