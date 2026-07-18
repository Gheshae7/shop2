from django.db import models
from basic.base_model import BaseModel



class Category(BaseModel):
    """This class is for products categories."""
    
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='نام دسته بندی', unique=True)
    url_name = models.SlugField(max_length=120, null=False, blank=False, verbose_name='آدرس دسته بندی در url', unique=True)
    parent = models.ForeignKey(to='Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='دسته بندی والد', related_name='children_categories')
    image = models.ImageField(upload_to='category/image', null=True, blank=True, verbose_name='عکس دسته بندی', help_text='فقط برای دسته بندی های والد استفاده می شود')
    
    
    def __str__(self):
        parent = '/ والد' if self.parent is None else ''
        return f'{self.name} / {self.url_name} {parent}'
    
    
    class Meta: 
        db_table = 'categories'
        db_table_comment = 'This table for products` categories'
        ordering = ['is_active', 'name', 'url_name',]
        

class Brand(BaseModel):
    """This class is for products brands."""
    
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='نام برند', unique=True)
    url_name = models.SlugField(max_length=120, null=False, blank=False, verbose_name='آدرس برند در url', unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'brands'
        db_table_comment = 'This table for products` brands'
        ordering = ['is_active', 'name', 'url_name',]
