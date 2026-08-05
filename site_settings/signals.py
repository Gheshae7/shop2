from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
import os
from .models import SiteSettings, HeroSection


@receiver(post_delete, sender=SiteSettings)
def delete_image_in_delete(sender, instance, **kwargs):
    """When a record is deleted, I remove its corresponding photo to free up storage space."""
    
    if instance.logo:
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
                     

@receiver(post_delete, sender=HeroSection)
def delete_image_in_delete(sender, instance, **kwargs):
    """When a record is deleted, I remove its corresponding photo to free up storage space."""
    
    if instance.small_image:
        if os.path.isfile(instance.small_image.path):
            os.remove(instance.big_image.path)
            
    if instance.big_image:
        if os.path.isfile(instance.big_image.path):
            os.remove(instance.big_image.path)


@receiver(pre_save, sender=HeroSection)   
def delete_image_in_modify(sender, instance, **kwargs):
    """When a record is edited, if the image has changed, I delete the previous image and replace it with the new one."""
    
    if not instance.pk:
        pass
    try:
        current_hero_section = HeroSection.objects.get(pk=instance.pk)
    except HeroSection.DoesNotExist:
        return
    
    if current_hero_section.small_image != instance.small_image:
        if current_hero_section.small_image and os.path.isfile(current_hero_section.small_image.path):
            os.remove(current_hero_section.small_image.path)

    if current_hero_section.big_image != instance.big_image:
        if current_hero_section.big_image and os.path.isfile(current_hero_section.big_image.path):
            os.remove(current_hero_section.big_image.path)
        