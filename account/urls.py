from django.urls import path
from .views import LoginRegisterView, login_account, register_account, activate_account, logout_account, ForgetPassword, ResetPassword, ProfileView

app_name = 'account'


urlpatterns = [
    path('', LoginRegisterView.as_view(), name='login_register_page'),
    path('login', login_account, name='login_account'),
    path('register', register_account, name='register_account'),
    path('logout', logout_account, name='logout_account'),
    path('forget-password', ForgetPassword.as_view(), name='forget_password_page'),
    path('activate/<str:email_active_code>', activate_account, name='activate_account'),
    path('reset-password/<str:email_active_code>', ResetPassword.as_view(), name='reset_password_page'),
    path('profile', ProfileView.as_view(), name='profile_page'),
]
