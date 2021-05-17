from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User # sender
from django.dispatch import receiver
from test_app.models import Notification
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, created, **kwargs):
#     instance.profile.save()

@receiver(pre_save, sender=Profile)
def delete_old_image(sender, instance, *args, **kwargs):
    try:
        old_img = Profile.objects.get(user=instance.user).image.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                if '\\media\\default.jpg' not in old_img:
                    os.remove(old_img)
    except:
        pass