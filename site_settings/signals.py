from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
import os
from .models import SiteSettings


@receiver(post_delete, sender=SiteSettings)
def delete_image_in_delete(sender, instance, **kwargs):
    """When a record is deleted, I remove its corresponding photo to free up storage space."""
    
    if instance.image:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)
            

@receiver(pre_save, sender=SiteSettings)   
def delete_image_in_modify(sender, instance, **kwargs):
    """When a record is edited, if the image has changed, I delete the previous image and replace it with the new one."""
    
    if not instance.pk:
        pass
    try:
        current_site_setting = SiteSettings.objects.get(pk=instance.pk)
    except SiteSettings.DoesNotExist:
        return
    if current_site_setting.logo != instance.logo:
        if current_site_setting.logo and os.path.isfile(current_site_setting.logo.path):
            os.remove(current_site_setting.logo.path)