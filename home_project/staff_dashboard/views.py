from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User

# staff_dashboard/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from order_app.models import Order
from .forms import OrderUpdateForm

def is_staff_user(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff_user)
def order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'staff_dashboard/order_list.html', {'orders': orders})

@login_required
@user_passes_test(is_staff_user)
def staff_order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    items = order.items.all()  # From related_name in Order_items
    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('staff_order_list')
    else:
        form = OrderUpdateForm(instance=order)
    return render(request, 'staff_dashboard/order_detail.html', {
        'order': order,
        'items': items,
        'form': form
    })


