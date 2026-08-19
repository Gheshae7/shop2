import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import NewsletterSubscriber




def add_email_to_newsletter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        new_newsletter, created = NewsletterSubscriber.objects.get_or_create(is_active=True, email=email)
        if created:
            return JsonResponse({
                'icon': 'success',
                'title': 'ایمیل شما برای عضویت در خبرنامه ثبت شد'
            })
        else:
            return JsonResponse({
                'icon': 'info',
                'title': 'ایمیل شما قبلا ثبت شده است'
            })
