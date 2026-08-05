from django.db import models
from basic.base_model import BaseModel
from django.utils.translation import gettext_lazy as _
from product.models import Product


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


class QuestionAnswer(BaseModel):
    """This class is for frequently asked questions from across the entire site."""
    
    class Positions(models.TextChoices):
        product_detail = "product_detail", _("صفحه جزییات محصول")
        home = "home", _("صفحه اصلی")
        
    
    question = models.TextField(verbose_name='پرسش')
    answer = models.TextField(verbose_name='پاسخ')
    emoji = models.CharField(max_length=10, null=True, blank=True, verbose_name='ایموجی این سوال', help_text='حتما پر شود و گرنه ظاهر سایت خراب می شود اگر پوزیشن محصول برای جزییات محصول هست نیازی نیست این قسمت پر شود')
    product = models.ManyToManyField(Product, verbose_name='این پرسش و پاسخ برای کدام محصول', help_text='اگر یک محصول یا محصولی نیاز به پرسش و پاسخ خاصی دارد حتما اینجا وارد کن اون محصول رو', related_name='quesions', blank=True)
    position = models.CharField(choices=Positions, null=False, blank=False, verbose_name='کجای صفحه قرار بگیرد', help_text='حتما این رو انتخاب کن که داحل کدوم صفحه نمایش داده بشه خیلی ممنون.')
    
    
    def __str__(self):
        return self.question
    
    
    class Meta:
        db_table = 'question_answers'
        db_table_comment = 'This table is for project-wide questions and answers.'
        ordering = ['is_active']
        
        
class Feature(BaseModel):
    """This class is used for the feature bar."""
    
    class Positions(models.TextChoices):
        products = "products", _("صفحه محصولات")
        home = "home", _("صفحه اصلی")
    
    title = models.CharField(max_length=55, null=False, blank=False, verbose_name='عنوان')
    description = models.CharField(max_length=255, null=False, blank=False, verbose_name='توضیحات')
    emoji = models.CharField(max_length=10, null=False, blank=True, verbose_name='اموجی', help_text='این رو اصن بزار نزاری باختی قافله رو')
    position = models.CharField(choices=Positions, null=False, blank=False, verbose_name='کجای صفحه قرار بگیرد', help_text='حتما این رو انتخاب کن که داحل کدوم صفحه نمایش داده بشه خیلی ممنون.')
    
    
    def __str__(self):
        return self.title
    
    
    class Meta:
        db_table = 'features'
        db_table_comment = 'This class is used for the feature bar.'
        ordering = ['is_active',]
        

class Ticker(BaseModel):
    """This model is used for that purple bar on the main screen."""
    
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='متن نمایش')
    
    
    def __str__(self):
        return self.title
    
    
    class Meta:
        db_table = 'tickers'
        db_table_comment = 'This table is used for that purple bar on the main screen.'
        ordering = ['is_active']
        

class HeroSection(BaseModel):
    """This class is for the upper section of the site, below the header."""
    
    short_title = models.CharField(max_length=35, null=False, blank=False, verbose_name='عنوان کوتاه')
    main_title = models.CharField(max_length=120, null=False, blank=False, verbose_name='عنوان اصلی')
    description = models.CharField(max_length=350, null=False, blank=False, verbose_name='توضیحات')
    btn_text = models.CharField(max_length=55, null=False, blank=False, verbose_name='متن درون دکمه')
    btn_url = models.CharField(max_length=512, null=False, blank=False, verbose_name='url دکمه')
    small_image = models.ImageField(upload_to='site_setting/hero_section', null=False, blank=False, verbose_name='عکس کوچک')
    big_image = models.ImageField(upload_to='site_setting/hero_section', null=False, blank=False, verbose_name='عکس بزرگ')
    
    
    def __str__(self):
        return self.short_title
    
    
    class Meta:
        ordering = ['is_active', 'updated_at']
        db_table = 'hero_section'
        db_table_comment = 'This table is for the upper section of the site, below the header.'
