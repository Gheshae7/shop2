from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string



class User(AbstractUser):
    """This is the user class, to which I've added a few fields."""
    
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    avatar = models.ImageField(upload_to='users/avatar', null=True, blank=True, verbose_name='آواتار')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='شماره تلفن')
    email_active_code = models.CharField(max_length=128, null=False, blank=False, verbose_name='کد فعالسازی حساب کاربری')
    
    
    def __str__(self):
        return f'{self.username} / {self.email}'
    
    
    class Meta:
        db_table = 'accounts'
        db_table_comment = 'User information is located in this table.'
        ordering = ['is_active']