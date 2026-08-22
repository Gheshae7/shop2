from django.db import models
from basic.base_model import BaseModel


class ContactUs(BaseModel):
    """This class handles the interaction between the user and the site."""
    
    full_name = models.CharField(max_length=65, null=False, blank=False, verbose_name='نام و نام خانوادگی')
    email = models.EmailField(max_length=100, null=False, blank=False, verbose_name='ایمیل')
    phone = models.CharField(max_length=11, null=False, blank=False, verbose_name='شماره تلفن')
    subject = models.CharField(max_length=100, null=False, blank=False, verbose_name='موضوع پیام')
    message = models.TextField(null=False, blank=False, verbose_name='متن پیام')
    is_read_by_admin = models.BooleanField(default=False, verbose_name='خوانده شده - نشده توسط ادمین')
    
    
    def __str__(self):
        return self.email
    
    
    class Meta:
        db_table = 'contacts_us'
        db_table_comment = 'This table handles the interaction between the user and the site.'
        ordering= ['is_active', 'email']