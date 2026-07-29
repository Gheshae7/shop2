from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Category, ProductsImages
import os


# region category
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
# endregion category            
      
      
# region ProductsImages
@receiver(post_delete, sender=ProductsImages)
def delete_image_in_delete(sender, instance, **kwargs):
    """When a record is deleted, I remove its corresponding photo to free up storage space."""
    
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
            

@receiver(pre_save, sender=ProductsImages)   
def delete_image_in_modify(sender, instance, **kwargs):
    """When a record is edited, if the image has changed, I delete the previous image and replace it with the new one."""
    
    if not instance.pk:
        pass
    try:
        current_product_image = ProductsImages.objects.get(pk=instance.pk)
    except ProductsImages.DoesNotExist:
        return
    if current_product_image.image != instance.image:
        if current_product_image.image and os.path.isfile(current_product_image.image.path):
            os.remove(current_product_image.image.path) 
# endregion ProductsImages
