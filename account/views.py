from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.views import View
from .forms import LoginForm, RegisterForm



class LoginRegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        login_form = LoginForm()
        register_form = RegisterForm()
        context = {
            'login_form': login_form,
            'register_form': register_form,
        }
        return render(request, 'account/login_register.html', context)