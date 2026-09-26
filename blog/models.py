from django.db import models
from basic.base_model import BaseModel
from django.utils.text import slugify
from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _



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
    category = models.ForeignKey(BlogCategory, verbose_name='دسته بندی ها', related_name='blogs_c', on_delete=models.SET_NULL, null=True)
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
    
    blog = models.ForeignKey(Blog, null=False, blank=False, on_delete=models.CASCADE, verbose_name='بلاگ', related_name='blog_sections')
    title = models.CharField(max_length=250, null=False, blank=False, verbose_name='عنوان این بخش از مقاله')
    content = models.TextField(verbose_name='توضیحات یا متن این قسمت')
    order = models.PositiveSmallIntegerField(verbose_name='ترتیب نمایش', help_text='عددی که بالاتر می باشد الویت بیشتری دارد')
    
    
    def __str__(self):
        return self.blog.name
    
    
    class Meta:
        db_table = 'blog_sections'
        db_table_comment = 'This table is for the various sections of a blog.'
        ordering = ['-order']
        
        
class BlogView(BaseModel):
    """This class is for counting the number of views for a blog."""
    
    ip = models.GenericIPAddressField(verbose_name='آدرس کاربر')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='کدام بلاک', related_name='count_views')
    
    
    def __str__(self):
        return f'{self.blog.name} / {self.ip}'
    
    
    class Meta:
        db_table = 'blog_views'
        db_table_comment = 'This table is for counting the number of views for a blog.'
        ordering = ['is_active']
 
 
class BlogLike(BaseModel):
    """This class is for counting the number of likes for a blog."""
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='کاربر')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='کدام بلاک', related_name='count_likes')
    
    
    def __str__(self):
        return f'{self.blog.name} / {self.user.email}'
    
    
    class Meta:
        db_table = 'blog_likes'
        db_table_comment = 'This table is for counting the number of likes for a blog.'
        ordering = ['is_active']
   

class BlogComment(BaseModel):
    """This class is for a blog's comments."""
    
    blog = models.ForeignKey(Blog, null=False, blank=False, on_delete=models.CASCADE, verbose_name='بلاگ', related_name='blog_comments')
    text = models.TextField(max_length=255, null=False, blank=False, verbose_name='متن کامنت')
    rating = models.SmallIntegerField(validators=(MaxValueValidator(5), MinValueValidator(0)), verbose_name='امتیاز',)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='کاربر', help_text='اگر کاربری که در سایت ثبت نام کرده باشد و این کامنت را بگذارد این مقدار پر می شود')
    name = models.CharField(max_length=100, null=True, blank=True, default='ناشناس', verbose_name='نام نویسنده', help_text='اگر کسی در سایت ما ثبت نام نکرده باشد و سپس کامنت بزاره ما اسمش رو از اینحا میزاریم اگر اسم پر نکنه به عنوان ناشناس این رو نشون میدیم')
    
    
    def __str__(self):
        return f'{self.pk} / {self.blog}'
    
    
    class Meta:
        db_table = 'comments_blogs'
        db_table_comment = 'This table is for blog comments.'
        ordering = ['is_active', '-created_at']
        

class BlogCommentReaction(BaseModel):
    """This table is for comment reactions"""
    
    class ReactionType(models.TextChoices):
        LIKE = 'like', 'like'
        DISLIKE = 'dislike', 'dislike'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        BlogComment,
        on_delete=models.CASCADE,
        related_name='blog_reactions'
    )
    reaction = models.CharField(
        max_length=10,
        choices=ReactionType.choices
    )
    
    def __str__(self):
        return f'{self.user} / {self.reaction}'
    
    
    class Meta:
        ordering = ['is_active', 'updated_at']
        db_table = 'comment_reactions_blog'
        db_table_comment = 'This table is for comment reactions' 
                   