import os 
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Contacts

@receiver(pre_delete, sender=Contacts)
def delete_profile_picture(sender, instance, **kwargs):
    if instance.profile_picture.name != 'profile_pictures/default.jpg':
        os.remove(os.path.join(settings.MEDIA_ROOT, instance.profile_picture.name))
