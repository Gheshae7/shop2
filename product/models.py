from django.db import models
from basic.base_model import BaseModel



class Category(BaseModel):
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='نام دسته بندی')
    url_name = models.SlugField(max_length=120, null=False, blank=False, verbose_name='آدرس دسته بندی در url')
    parent = models.ForeignKey(to='Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='دسته بندی والد')
    image = models.ImageField(upload_to='category/image', null=True, blank=True, verbose_name='عکس دسته بندی', help_text='فقط برای دسته بندی های والد استفاده می شود')
    
    
    class Meta: 
        db_table = 'categories'
        db_table_comment = 'This table for products` categories'
        ordering = ['is_active', 'name', 'url_name',]