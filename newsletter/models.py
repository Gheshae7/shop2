from django.db import models
from basic.base_model import BaseModel
# Create your models here.



class NewsletterSubscriber(BaseModel):
    """This class is for users who want to subscribe to the newsletter."""
    
    email = models.EmailField(unique=True, null=False, blank=False, verbose_name='ایمیل')
    
    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'news_letter_subscribers'
        db_table_comment = 'This table is for users who want to subscribe to the newsletter.'
        ordering = ['is_active', 'email']