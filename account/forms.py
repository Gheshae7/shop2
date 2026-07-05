from django import forms 
from django.core import validators

class LoginForm(forms.Form):
    email = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'مثال: example@gmail.com',
        'class': 'w-full bg-white/50 backdrop-blur-sm border border-slate-200 text-slate-800 rounded-2xl px-5 py-3.5 outline-none focus:bg-white focus:border-blue-300 focus:shadow-[0_0_0_4px_rgba(59,130,246,0.1)] transition-all duration-500 placeholder:text-slate-400',
        'type': 'text',
    }))
    
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        'placeholder': '••••••••',
        'class': 'w-full bg-white/50 backdrop-blur-sm border border-slate-200 text-slate-800 rounded-2xl px-5 py-3.5 outline-none focus:bg-white focus:border-blue-300 focus:shadow-[0_0_0_4px_rgba(59,130,246,0.1)] transition-all duration-500 placeholder:text-slate-400',
        'type': 'password',    
    }),)
    
    
    
class RegisterForm(forms.Form):
    email = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'ایمیل',
        'class': 'w-full bg-white/50 backdrop-blur-sm border border-slate-200 text-slate-800 rounded-2xl px-5 py-3.5 outline-none focus:bg-white focus:border-purple-300 focus:shadow-[0_0_0_4px_rgba(168,85,247,0.1)] transition-all duration-500 placeholder:text-slate-400',
        'type': 'text',
    }))
    
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'رمز عبور',
        'class': 'w-full bg-white/50 backdrop-blur-sm border border-slate-200 text-slate-800 rounded-2xl px-5 py-3.5 outline-none focus:bg-white focus:border-purple-300 focus:shadow-[0_0_0_4px_rgba(168,85,247,0.1)] transition-all duration-500 placeholder:text-slate-400',
        'type': 'password',    
    }), validators=[validators.MinLengthValidator(8), validators.MaxLengthValidator(100)])
    
    
    confirm_password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'تکرار رمز عبور',
        'class': 'w-full bg-white/50 backdrop-blur-sm border border-slate-200 text-slate-800 rounded-2xl px-5 py-3.5 outline-none focus:bg-white focus:border-purple-300 focus:shadow-[0_0_0_4px_rgba(168,85,247,0.1)] transition-all duration-500 placeholder:text-slate-400',
        'type': 'password',    
    }), validators=[validators.MinLengthValidator(8), validators.MaxLengthValidator(100)])