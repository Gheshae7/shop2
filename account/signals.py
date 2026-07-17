from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import User
import os


@receiver(post_delete, sender=User)
def delete_avatar_in_delete(sender, instance, **kwargs):
    '''When a record is deleted, I remove its corresponding photo to free up storage space.'''

    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)
            
            

@receiver(pre_save, sender=User)
def delete_avatar_in_modify(sender, instance, **kwargs):
    """When a record is edited, if the image has changed, I delete the previous image and replace it with the new one."""

    if not instance.pk:
        pass
    try:
        current_user = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return
    if current_user.avatar != instance.avatar:
        if current_user.avatar and os.path.isfile(current_user.avatar.path):
            os.remove(current_user.avatar.path)
            