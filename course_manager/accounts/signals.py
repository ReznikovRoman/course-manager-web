from django.dispatch import receiver
from django.db.models.signals import (post_save, )

from . import models

#######################################################################################################################


@receiver(post_save, sender=models.CustomUser)
def create_profile(sender, instance, created: bool, **kwargs):
    if created:
        models.Profile.objects.create(
            user=instance
        )


@receiver(post_save, sender=models.CustomUser)
def update_profile(sender, instance, created: bool, **kwargs):
    if not created:
        instance.profile.save()











