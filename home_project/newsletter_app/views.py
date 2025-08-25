
from django.shortcuts import render, redirect
from .forms import NewsletterForm
from django.contrib import messages

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import NewsletterSubscriber
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@csrf_exempt  # we'll handle CSRF token in JS
def subscribe_newsletter_ajax(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success", "message": "Thank you for subscribing!"})
        else:
            return JsonResponse({"status": "error", "message": "This email is already subscribed or invalid."})
    return JsonResponse({"status": "error", "message": "Invalid request."})

@login_required
def newsletter_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Not authorized")
    subscribers = NewsletterSubscriber.objects.all().order_by('-subscribed_at')
    if not subscribers.exists():
        print("No subscribers found!")
    print("subscribers 123",subscribers)
    return render(request, 'newsletter/newsletter.html', {'subscribers': subscribers})