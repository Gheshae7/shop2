from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
import json
from django.http import JsonResponse
from .models import ContactUs
from django.contrib import messages
from site_settings.models import SiteSettings, QuestionAnswer



class ContactUsView(TemplateView):
    template_name = 'contact/contact_us.html'
    
    def post(self, request, *args, **kwargs):
        data_contact = json.loads(request.body)
        if data_contact is not None:
            ContactUs.objects.create(full_name=data_contact.get('name'), email=data_contact.get('email'), phone=data_contact.get('phone'), subject=data_contact.get('subject'), message=data_contact.get('message'), is_read_by_admin=False)
            
            return JsonResponse({
                'success': 'true',
            })
        else:
            messages.error(self.request, 'مشکلی پیش آمد. مجدد امتحان کنید')
            return redirect(reverse('contact:contact_us_page'))
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_setting'] = SiteSettings.objects.filter(is_active=True).values('support_email', 'phone', 'instagram_channel', 'x_channel')[:1]
        context['questions'] = QuestionAnswer.objects.filter(is_active=True, position='contact').values('question', 'answer', 'position', 'id')
        return context
