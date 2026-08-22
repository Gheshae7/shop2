from django.shortcuts import render
from django.views.generic import TemplateView



class ContactUsView(TemplateView):
    template_name = 'contact/contact_us.html'