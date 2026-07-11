from django import forms 
from django.core import validators
from account.models import User

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
    
    
    
    
class ForgetForm(forms.Form):
    email = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'placeholder': 'مثال: example@gmail.com',
        'class': 'w-full bg-white/50 backdrop-blur-sm border border-slate-200 text-slate-800 rounded-2xl px-5 py-3.5 outline-none focus:bg-white focus:border-purple-300 focus:shadow-[0_0_0_4px_rgba(168,85,247,0.1)] transition-all duration-500 placeholder:text-slate-400',
        'type': 'text',
    }))
    
    
    
class ResetForm(forms.Form):
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



class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'phone', 'avatar']
        
        lable = {
            'username': 'نام کاربری',
            'email': 'ایمیل',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'avatar': 'پروفایل',
            'address': 'آدرس',
            'phone': 'تلفن',
        }
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
                'type': 'text'
            }),
            'email': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
                'type': 'text'
            }), 
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
                'type': 'text'
            }),   
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
                'type': 'text'
            }),   
            'address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
                'type': 'text'
            }),   
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-violet-400 transition-colors',
                'type': 'text'
            }), 
                                                                                  
        }
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields["email"].disabled = True