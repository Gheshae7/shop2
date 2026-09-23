from django.db import models
from basic.base_model import BaseModel
from django.utils.text import slugify



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
        

class Blog(BaseModel):
    """This class is for posts or blogs."""
    
    name = models.CharField(max_length=450, null=False, blank=False, unique=True, verbose_name='نام مقاله')
    category = models.ManyToManyField(BlogCategory, verbose_name='دسته بندی ها', related_name='blogs_c')
    tag = models.ManyToManyField(BlogTag, verbose_name='تگ ها', related_name='blogs_t')
    short_text = models.CharField(max_length=600, null=False, blank=False, verbose_name='توضیحات کوتاه')
    summary = models.TextField(null=False, blank=False, verbose_name='خلاصه بلاگ')
    reading_time = models.PositiveSmallIntegerField(verbose_name='مدت زمان مطالعه', null=False, blank=False)
    image = models.ImageField(upload_to='blog/image/', verbose_name='عکس بلاگ', null=False, blank=False)
    slug = models.SlugField(max_length=550, null=False, blank=True, verbose_name='آدرس url در بلاگ')
    
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.name
    
    
    class Meta:
        db_table = 'blogs'
        db_table_comment = 'This table is for posts or blogs.'
        ordering = ['name']

        
class BlogSection(BaseModel):
    """This class is for the various sections of a blog."""
    
    blog = models.ForeignKey(Blog, null=False, blank=False, on_delete=models.CASCADE, verbose_name='بلاگ')
    title = models.CharField(max_length=250, null=False, blank=False, verbose_name='عنوان این بخش از مقاله')
    content = models.TextField(verbose_name='توضیحات یا متن این قسمت')
    order = models.PositiveSmallIntegerField(verbose_name='ترتیب نمایش', help_text='عددی که بالاتر می باشد الویت بیشتری دارد')
    
    
    def __str__(self):
        return self.blog
    
    
    class Meta:
        db_table = 'blog_sections'
        db_table_comment = 'This table is for the various sections of a blog.'
        ordering = ['-order']