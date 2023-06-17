from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User,UserProfile

@receiver(post_save,sender=User)   
def create_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            instance.userprofile.save()
        except:
            UserProfile.objects.create(user=instance)

@receiver(pre_save,sender=User)
def pre_save_profile(sender,instance,**kwargs):
    pass  