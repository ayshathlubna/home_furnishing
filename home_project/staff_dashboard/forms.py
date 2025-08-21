from django import forms
from order_app.models import Order

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'payment_status',
            'delivery_status',
            'refund_status',
            'refund_amount',
            'delivery_date'
        ]