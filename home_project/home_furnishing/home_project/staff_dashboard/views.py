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
        # All pending cancellation and return requests
        context['requests'] = Order_items.objects.filter(
            refund_status__in=['cancellation_requested', 'return_requested']
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
@login_required
def staff_order_detail(request, order_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Not authorized")

    order = get_object_or_404(Order, order_id=order_id)
    items = order.items.all()

    if request.method == "POST":
        for item in items:
            delivery_status = request.POST.get(f"delivery_status_{item.id}")
            refund_status = request.POST.get(f"refund_status_{item.id}")
            
            if delivery_status:
                item.delivery_status = delivery_status
            if refund_status:
                item.refund_status = refund_status
            item.save()

        # Update order-level refund status
        refunded_items = items.filter(refund_status="Completed").count()
        total_items = items.count()
        if refunded_items == 0:
            order.refund_status = "Not Requested"
        elif refunded_items < total_items:
            order.refund_status = "Partially Refunded"
        else:
            order.refund_status = "Refunded"

        # Update payment status if online payment
        if order.payment_method != "Cash on Delivery":
            if order.refund_status == "Refunded":
                order.payment_status = "Refunded"
            elif order.refund_status == "Partially Refunded":
                order.payment_status = "Paid"

        order.save()
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

    # Handle cancellation request
    if item.refund_status == "cancellation_requested":
        item.delivery_status = "Cancelled"
        item.refund_status = "Completed"
        item.product.stock = F('stock') + item.quantity
        item.product.save()

    # Handle return request
    elif item.refund_status == "return_requested":
        item.refund_status = "Completed"
        item.product.stock = F('stock') + item.quantity
        item.product.save()

    item.save()

    # Update order refund status
    order = item.order
    refunded_items = order.items.filter(refund_status="Completed").count()
    total_items = order.items.count()
    order.refund_status = "Partially Refunded" if refunded_items < total_items else "Refunded"
    order.save()

    return redirect("staff_order_detail", order_id=item.order.order_id)


# -------------------------------
# Reject Cancel / Return Request
# -------------------------------
@login_required
def reject_request(request, item_id):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Not authorized")

    item = get_object_or_404(Order_items, id=item_id)
    item.refund_status = "Rejected"
    item.save()

    return redirect("staff_order_detail", order_id=item.order.order_id)


# -------------------------------
# Centralized Requests List
# -------------------------------
@login_required
def requests_dashboard(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Not authorized")

    # Combine cancellation and return requests
    requests = Order_items.objects.filter(
        refund_status__in=['cancellation_requested', 'return_requested']
    ).order_by('-order__order_date')

    return render(request, "staff_dashboard/requests_dashboard.html", {"requests": requests})
