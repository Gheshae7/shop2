from django.db import models


class BaseModel(models.Model):
    """This function is for models that have duplicate fields."""
    
    is_active = models.BooleanField(default=True, verbose_name='فعال - غیر فعال', null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین آپدیت')
    
    class Meta:
        ordering = ['is_active']
        abstract = True