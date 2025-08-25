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
    payment_status = models.CharField(max_length=20, choices=payment_status_choices, default='Pending')

    status_choices = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Refunded','Refunded'),
        ('Partially Refunded','Partially Refunded')
    ]
    delivery_status = models.CharField(max_length=25, choices=status_choices, default='Pending')

    order_date = models.DateField(auto_now_add=True)

    # 🔹 Track refund at order level
    refund_status_choices = [
        ('Not Requested', 'Not Requested'),
        ('Partially Refunded', 'Partially Refunded'),
        ('Refunded', 'Refunded'),
    ]
    refund_status = models.CharField(max_length=20, choices=refund_status_choices, default='Not Requested')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.order_id)

    # ✅ Aggregates item refunds into order refund status
    def update_refund_status(self):
        refunded_items = self.items.filter(refund_status="Completed").count()
        total_items = self.items.count()
        if refunded_items == 0:
            self.refund_status = "Not Requested"
        elif refunded_items < total_items:
            self.refund_status = "Partially Refunded"
        else:
            self.refund_status = "Refunded"

        # Auto update payment status if online payment
        if self.payment_method != "Cash on Delivery":
            if self.refund_status == "Refunded":
                self.payment_status = "Refunded"
            elif self.refund_status == "Partially Refunded":
                self.payment_status = "Paid"

        self.save()


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
        ('Returned','Returned'),
    ]
    delivery_status = models.CharField(max_length=25, choices=status_choices, default='Pending')

    payment_status_choices = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Refunded', 'Refunded'),
        ('Cancelled','Cancelled')
    ]
    payment_status = models.CharField(max_length=20, choices=payment_status_choices, default='Pending')

    refund_status_choices = [
        ('Not Requested', 'Not Requested'),
        ('Requested', 'Requested'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]
    refund_status = models.CharField(max_length=20, choices=refund_status_choices, default='Not Requested')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    return_requested = models.BooleanField(default=False)

    def can_return(self):
        """ Allow return if delivered and within 7 days. """
        if self.delivery_status == "Delivered" and self.order.delivery_date:
            return timezone.now().date() <= (self.order.delivery_date + timedelta(days=7))
        return False

    def __str__(self):
        return f"{self.product} x {self.quantity}"
