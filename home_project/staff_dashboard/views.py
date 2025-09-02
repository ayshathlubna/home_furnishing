from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import F, Q
from order_app.models import Order, Order_items
from newsletter_app.models import NewsletterSubscriber

# -------------------------------
# Staff Dashboard
# -------------------------------
@login_required
def staff_dashboard(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Not authorized")

    section = request.GET.get('section', 'default')
    context = {"section": section}

    if section == 'newsletter':
        context['subscribers'] = NewsletterSubscriber.objects.all()
    elif section == 'orders':
        context['orders'] = Order.objects.all().order_by('-order_date')
    elif section == 'requests':
        # All pending cancellation and return requests now share the 'Requested' status
        context['requests'] = Order_items.objects.filter(
            Q(delivery_status='Cancellation Requested') |  Q(delivery_status='Return Requested')
        ).order_by('-order__order_date')

    return render(request, 'staff_dashboard/staff_dashboard.html', context)


# -------------------------------
# Staff Order List / Search
# -------------------------------
@login_required
def order_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Not authorized")

    orders = Order.objects.all().order_by("-order_date")
    query = request.GET.get("q")
    status_filter = request.GET.get("status")
    
    if query:
        orders = orders.filter(Q(user__username__icontains=query) | Q(order_id__icontains=query))
    if status_filter:
        orders = orders.filter(delivery_status=status_filter)
    
    return render(request, "staff_dashboard/order_list.html", {"orders": orders})


# -------------------------------
# Staff Order Detail
# -------------------------------
# staff_dashboard/views.py
from django.utils import timezone
# ... other imports

# -------------------------------
# Staff Order Detail
# -------------------------------
@login_required
def staff_order_detail(request, order_id):
    # ... (authorization check)

    order = get_object_or_404(Order, order_id=order_id)
    items = order.items.all()

    if request.method == "POST":
        for item in items:
            delivery_status = request.POST.get(f"delivery_status_{item.id}")
            payment_status = request.POST.get(f"payment_status_{item.id}")
            refund_status = request.POST.get(f"refund_status_{item.id}")

            # Check if the status is changing to 'Delivered'
            if delivery_status == "Delivered" and item.delivery_date is None:
                item.delivery_date = timezone.now().date()

            # Update other statuses as before
            if delivery_status:
                item.delivery_status = delivery_status
            # ... (other updates, e.g., refund_status)

            if payment_status:
                item.payment_status = payment_status

            if refund_status:
                item.refund_status = refund_status
            item.save()

        return redirect("staff_order_detail", order_id=order_id)

    return render(request, "staff_dashboard/order_detail.html", {"order": order, "items": items})
# -------------------------------
# Approve Cancel / Return Request
# -------------------------------
@login_required
def approve_request(request, item_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Not authorized")

    item = get_object_or_404(Order_items, id=item_id)
    order = item.order
    
    # Calculate the proportional share of fees
    total_quantity = order.total_quantity
    if total_quantity > 0:
        fee_per_item = (order.platform_fee + order.delivery_charge) / total_quantity
    else:
        fee_per_item = 0

    # Calculate the refund amount for this specific item
    calculated_refund_amount = item.total_amount + fee_per_item

    if item.delivery_status == "Cancellation Requested":
        # Handle cancellation approval
        item.delivery_status = "Cancelled"
       
        if item.order.payment_method != "Cash on Delivery":
            item.payment_status = "Refunded"
            item.refund_status = "Completed"
            item.refund_amount = calculated_refund_amount
        else:
            item.payment_status = "Cancelled"
        
        # Add stock back to the product
        item.product.stock = F('stock') + item.quantity
        item.product.save()

    elif item.delivery_status == "Return Requested":
        # Handle return approval
        item.delivery_status = "Returned"
        item.payment_status = "Refunded"
        item.refund_status = "Completed"
        item.refund_amount = calculated_refund_amount
        
        # Add stock back to the product
        item.product.stock = F('stock') + item.quantity
        item.product.save()
    else:
        # Request is not in a valid state to be approved
        return redirect("staff_dashboard")

    # Save the order item with the new status and refund amount
    item.save()

    return redirect("staff_order_detail", order_id=order.order_id)
# -------------------------------
# Reject Cancel / Return Request
# -------------------------------
@login_required
def reject_request(request, item_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Not authorized")

    item = get_object_or_404(Order_items, id=item_id)
    
    # Check the type of request to revert the delivery status correctly
    if item.delivery_status == "Cancellation Requested":
        item.delivery_status = "Pending"
    elif item.delivery_status == "Return Requested":
        item.delivery_status = "Delivered"

    item.refund_status = "Rejected"
    item.save() # This save call will trigger the parent Order update

    return redirect("staff_order_detail", order_id=item.order.order_id)