from django.db import models
from basic.base_model import BaseModel


class FooterBox(BaseModel):
    """This class is for categorizing the site's footer links"""
    name = models.CharField(max_length=155, null=False, blank=False, verbose_name='نام دسته')
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        db_table = 'footer_boxes'
        db_table_comment = "This table is for categorizing the site's footer links"

        
class FooterLink(BaseModel):
    """This class is for the site's footer links and is related to the class mentioned above."""
    
    name = models.CharField(max_length=155, null=False, blank=False, verbose_name='نام لینک')
    url = models.CharField(max_length=512, null=True, blank=True, verbose_name='آدرس url')
    footer_box = models.ForeignKey(FooterBox, on_delete=models.SET_NULL, null=True, blank=True, related_name='footer_links')
    
    
    def __str__(self):
        return f'{self.name} / {self.footer_box.name}'
    
    
    class Meta:
        ordering = ['name']
        db_table = 'footer_links'
        db_table_comment = "This table is for the site's footer links."


class SiteSettings(BaseModel):
    """This class displays site settings, such as the site logo, copyright text, etc."""
    
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name='نام سایت')
    logo = models.ImageField(null=True, blank=True, verbose_name='لوگو سایت', upload_to='site_setting/logo')
    support_email = models.CharField(max_length=100, null=True, blank=True, verbose_name='ایمیل پشتیبانی')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='تلفن تماس')
    telegram_support = models.CharField(max_length=75, null=True, blank=True, verbose_name='آدرس پشتیبانی در تلگرام')
    copy_right = models.CharField(max_length=512, null=False, blank=False, verbose_name='متن کپی رایت')
    version = models.CharField(max_length=10, null=True, blank=True, verbose_name='ورژن سایت')
    site_slogan = models.CharField(max_length=255, null=True, blank=True, verbose_name='شعار سایت')
    telegram_channel = models.CharField(max_length=75, null=True, blank=True, verbose_name='آدرس کانال در تلگرام')
    instagram_channel = models.CharField(max_length=75, null=True, blank=True, verbose_name='آدرس اینستاگرام')
    linkedin_channel = models.CharField(max_length=75, null=True, blank=True, verbose_name='آدرس لینکدین')
    youtube_channel = models.CharField(max_length=75, null=True, blank=True, verbose_name='آدرس یوتیوب')
    x_channel = models.CharField(max_length=75, null=True, blank=True, verbose_name='آدرس ایکس')
    about_in_footer = models.CharField(max_length=300, null=True, blank=True, verbose_name='درباره ما در فوتر')
    support_status = models.BooleanField(default=True, null=False, blank=False, verbose_name='فعال - غیر فعال بودن پشتیبانی')
    
    
    def __str__(self):
        return f'{self.name} / {self.version}'
    
    class Meta:
        ordering = ['is_active' ,'name']
        db_table = 'site_settings'
        db_table_comment = 'This table displays site settings, such as the site logo, copyright text, etc.'
