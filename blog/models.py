from django.db import models
from basic.base_model import BaseModel



class BlogCategory(BaseModel):
    """This class is used for blog categories."""
    
    name = models.CharField(max_length=120, null=False, blank=False, verbose_name='نام دسته بندی', unique=True)
    url_name = models.SlugField(max_length=120, null=False, blank=False, verbose_name='آدرس دسته بندی در url', unique=True)
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        db_table = 'blog_categories'
        db_table_comment = 'This table is used for blog categories.'
        ordering = ['name']
        
        
class BlogTag(BaseModel):
    """This class is for blog tags."""
    
    name = models.CharField(max_length=100, unique=True, blank=False, name=False, verbose_name='نام تگ')
    
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        db_table = 'blog_tags'
        db_table_comment = 'The tags for the blogs are listed in this table.'
        ordering = ['name']
    