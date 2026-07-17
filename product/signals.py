from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Category
import os


@receiver(post_delete, sender=Category)
def delete_image_in_delete(sender, instance, **kwargs):
    """When a record is deleted, I remove its corresponding photo to free up storage space."""
    
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
            
            

@receiver(pre_save, sender=Category)
def delete_image_in_modify(sender, instance, **kwargs):
    """When a record is edited, if the image has changed, I delete the previous image and replace it with the new one."""
    
    if not instance.pk:
        pass
    try:
        current_category = Category.objects.get(pk=instance.pk)
    except Category.DoesNotExist:
        return
    if current_category.image != instance.image:
        if current_category.image and os.path.isfile(current_category.image.path):
            os.remove(current_category.image.path)