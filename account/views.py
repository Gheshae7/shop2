from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from .forms import LoginForm, RegisterForm, ForgetForm, ResetForm
from django.contrib import messages
from account.models import User
from django.contrib.auth import login, logout
from django.utils.crypto import get_random_string
from .tasks.send_emails import send_email


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
        # ]f the user is logged in
        if request.user.is_authenticated:
            messages.error(request, 'لطفا از اکانت خود خارج شوید و مجدد تست کنید')
            return redirect(reverse('account:login_register_page'))
        login_form: LoginForm = LoginForm(request.POST)
        if login_form.is_valid():
            try:
                # User login
                current_user: User = get_user(email=login_form.cleaned_data['email'])
                if current_user.check_password(login_form.cleaned_data['password']):
                    login(request, current_user)
                    messages.success(request, 'با موفقیت وارد حساب کاربری خود شده اید')
                    return redirect(reverse('home:home_page'))
                else:
                    # User not found
                    messages.error(request, 'کاربری با این مشخصات یافت نشد')
                    return redirect(reverse('account:login_register_page'))
            # Any error
            except User.DoesNotExist:
                messages.error(request, 'کاربری با این مشخصات یافت نشد یا حساب کاربری غیرفعال است')
                return redirect(reverse('account:login_register_page'))
 
  
  
def register_account(request: HttpRequest) -> HttpResponseRedirect:
    """This Function for registering users"""
    
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            try:
                # User Found so new user cannot be registered
                currrent_user = User.objects.get(email=register_form.cleaned_data.get('email'))
                messages.error(request, 'کاربری با این مشخصات وجود دارد')
                return redirect(reverse('account:login_register_page'))
            # User not found so new user can be regestered
            except User.DoesNotExist:
                password: str = register_form.cleaned_data.get('password')
                confirm_password: str = register_form.cleaned_data.get('confirm_password')
                # Checking password and confirm password 
                if password == confirm_password:
                    # Create and svae new user
                    new_user: User = User.objects.create(email=register_form.cleaned_data.get('email'), is_active=False)
                    new_user.set_password(password)
                    new_user.save(update_fields=['password'])
                    # Send an email to the user to activate their account.
                    send_email.apply_async(args=['فعالسازی حساب کاربری', new_user.email, {'email_active_code': new_user.email_active_code}, 'account/emails/activate_account.html'])
                    messages.success(request, 'حساب کاربری با موفقیت ساخته شد. جهت فعالسازی حساب کاربری خود به بخش صندوق دریافت ایمیل خود مراجعه کنید')
                    return redirect(reverse('account:login_register_page'))
                else:
                    # Password != confirm password
                    messages.error(request, 'رمز عبور و تکرار رمز عبور یکی نیستند لطفا دقت فرمایید')
                    return redirect(reverse('account:login_register_page'))
        else:
            # Any error
            messages.error(request, 'رمز عبور باید شامل حروف انگلیسی بزرگ و کوچک و عدد باشد')
            return redirect(reverse('account:login_register_page')) 



def activate_account(request: HttpRequest, email_active_code: str) -> HttpResponseRedirect:
    """This function for activate account users"""

    try:
        # activate user account
        current_user: User = User.objects.get(email_active_code__exact=email_active_code)
        current_user.is_active = True
        current_user.email_active_code = get_random_string(128)
        current_user.save()
        messages.success(request, 'حساب کاربری شما با موفقیت فعال شد')
        return redirect(reverse('account:login_register_page'))
    # User not found so cannot be activated account
    except User.DoesNotExist:
        messages.error(request ,'حساب کاربری پیدا نشد مجدد امتحان فرمایید')
        return redirect(reverse('account:login_register_page'))
    
    
    
def logout_account(request: HttpRequest) -> HttpResponseRedirect:
    """This function for logouting users"""
    
    # If the user is logged in, then log them out.
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'با موفقیت از حساب کاربری خود خارج شدید')
        return redirect(reverse('home:home_page')) 
    else:
        # Any error
        messages.error(request, 'شما اصلا در حساب کاربری خود نیستید که بخواهید از حساب خود خارج شوید')
        return redirect(reverse('account:login_register_page')) 



class ForgetPassword(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        forget_form = ForgetForm
        context = {
            'forget_form': forget_form
        }
        return render(request, 'account/forget_password.html', context)
    
    
    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            try:
                # User found so send email to user for reset password
                current_user = get_user(email=forget_form.cleaned_data.get('email'))
                send_email.apply_async(args=['بازیابی کلمه عبور', current_user.email, {'email_active_code': current_user.email_active_code}, 'account/emails/reset_password.html'])
                messages.success(request, 'ایمیلی جهت بازیابی کلمه عبور به شما ارسال شد')
                return redirect(reverse('account:login_register_page'))
            # User not found
            except User.DoesNotExist:
                messages.error(request, 'کاربری با این مشخصات وجود ندارد')
                return redirect(reverse('account:forget_password_page'))
        else:
            # Any error
            messages.error(request, 'مشکلی پیش آمد مجدد تست فرمایید')
            return redirect(reverse('account:forget_password_page'))



class ResetPassword(View):
    def get(self, request: HttpRequest, email_active_code: str) -> HttpResponse | HttpResponseRedirect:
        try:
            current_user = User.objects.get(email_active_code__exact=email_active_code, is_active=True)
            reset_form = ResetForm
            context = {
                'reset_form': reset_form,
                'user_email_active_code': email_active_code
            }
            return render(request, 'account/reset_password.html', context)
        except User.DoesNotExist:
            messages.error(request, 'کاربر مورد نظر پیدا نشد لطفا مجدد امتحان کنید')
            return redirect(reverse('account:forget_password_page'))        
        
    def post(self ,request: HttpRequest, email_active_code: str) -> HttpResponseRedirect:
        try: 
            # User found so user can be reset password
            current_user: User = User.objects.get(email_active_code__exact=email_active_code)
            reset_form = ResetForm(request.POST)
            if reset_form.is_valid():
                password = reset_form.cleaned_data.get('password')
                confirm_password = reset_form.cleaned_data.get('confirm_password')
                # Checking password and confirm password
                if password == confirm_password:
                    current_user.set_password(password)
                    current_user.email_active_code = get_random_string(128)
                    current_user.save()
                    messages.success(request, 'رمز عبور شما با موفقیت بازیابی شد')
                    return redirect(reverse('home:home_page'))
                else:
                    # Password != confirm password
                    messages.error(request, 'رمز عبور و تکرار رمز عبور یکی نیستند لطفا دقت فرمایید')
                    return redirect(reverse('account:reset_password_page', kwargs={'email_active_code': email_active_code}))
            else:
                # Any error
                messages.error(request, 'رمز عبور باید شامل حروف انگلیسی بزرگ و کوچک و عدد باشد')
                return redirect(reverse('account:reset_password_page', kwargs={'email_active_code': email_active_code}))

        except User.DoesNotExist:
            # User not found so user cannot be reset password
            messages.error(request, 'کاربر مورد نظر پیدا نشد لطفا مجدد امتحان کنید')
            return redirect(reverse('account:forget_password_page'))     
   