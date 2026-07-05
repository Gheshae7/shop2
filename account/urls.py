from django.urls import path
from .views import LoginRegisterView

app_name = 'account'


urlpatterns = [
    path('', LoginRegisterView.as_view(), name='login_register_page'),
]
