from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from account.models import User
from django.contrib.auth import login, logout
from django.utils.crypto import get_random_string


class LoginRegisterView(View):
    """This class is for displaying the user login and registration form"""
    
    def get(self, request: HttpRequest) -> HttpResponse:
        login_form: LoginForm = LoginForm()
        register_form: RegisterForm = RegisterForm()
        context = {
            'login_form': login_form,
            'register_form': register_form,
        }
        return render(request, 'account/login_register.html', context)
    
 
 
def get_user(email: str,) -> User:
    """This function for get user"""
    
    try:
        user: User = User.objects.get(email__exact=email, is_active=True)
        return user
    except User.DoesNotExist:
        raise User.DoesNotExist('کاربری پیدا نشد')
 
    
    
def login_account(request: HttpRequest) -> HttpResponseRedirect:
    """This function for logining users"""

    if request.method == 'POST':
        if request.user.is_authenticated:
            messages.error(request, 'لطفا از اکانت خود خارج شوید و مجدد تست کنید')
            return redirect(reverse('account:login_register_page'))
        login_form: LoginForm = LoginForm(request.POST)
        if login_form.is_valid():
            try:
                current_user: User = get_user(email=login_form.cleaned_data['email'])
                if current_user.check_password(login_form.cleaned_data['password']):
                    login(request, current_user)
                    messages.success(request, 'با موفقیت وارد حساب کاربری خود شده اید')
                    return redirect(reverse('home:home_page'))
                else:
                    messages.error(request, 'کاربری با این مشخصات یافت نشد')
                    return redirect(reverse('account:login_register_page'))
            except User.DoesNotExist:
                messages.error(request, 'کاربری با این مشخصات یافت نشد یا حساب کاربری غیرفعال است')
                return redirect(reverse('account:login_register_page'))
 
  
  
def register_account(request: HttpRequest) -> HttpResponseRedirect:
    """This Function for registering users"""
    
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            try:
                currrent_user = User.objects.get(email=register_form.cleaned_data.get('email'))
                messages.error(request, 'کاربری با این مشخصات وجود دارد')
                return redirect(reverse('account:login_register_page'))
            except User.DoesNotExist:
                password: str = register_form.cleaned_data.get('password')
                confirm_password: str = register_form.cleaned_data.get('confirm_password')
                if password == confirm_password:
                    new_user: User = User.objects.create(email=register_form.cleaned_data.get('email'), is_active=False)
                    new_user.set_password(password)
                    new_user.save(update_fields=['password'])
                    # TODO: send email
                    messages.success(request, 'حساب کاربری با موفقیت ساخته شد. جهت فعالسازی حساب کاربری خود به بخش صندوق دریافت ایمیل خود مراجعه کنید')
                    return redirect(reverse('account:login_register_page'))
                else:
                    messages.error(request, 'رمز عبور و تکرار رمز عبور یکی نیستند لطفا دقت فرمایید')
                    return redirect(reverse('account:login_register_page'))
        else:
            messages.error(request, 'رمز عبور باید شامل حروف انگلیسی بزرگ و کوچک و عدد باشد')
            return redirect(reverse('account:login_register_page')) 



def activate_account(request: HttpRequest, email_active_code: str) -> HttpResponseRedirect:
    """This function for activate account users"""

    try:
        current_user: User = User.objects.get(email_active_code__exact=email_active_code)
        current_user.is_active = True
        current_user.email_active_code = get_random_string(128)
        current_user.save()
        messages.success(request, 'حساب کاربری شما با موفقیت فعال شد')
        return redirect(reverse('account:login_register_page'))
    except User.DoesNotExist:
        messages.error(request ,'حساب کاربری پیدا نشد مجدد امتحان فرمایید')
        return redirect(reverse('account:login_register_page'))
    
    
    
def logout_account(request: HttpRequest) -> HttpResponseRedirect:
    """This function for logouting users"""
    
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'با موفقیت از حساب کاربری خود خارج شدید')
        return redirect(reverse('home:home_page')) 
    else:
        messages.error(request, 'شما اصلا در حساب کاربری خود نیستید که بخواهید از حساب خود خارج شوید')
        return redirect(reverse('account:login_register_page')) 
