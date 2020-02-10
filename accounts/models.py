from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from transactions.models import Wallet, Transaction


class Profile(models.Model):
    user = models.OneToOneField(User,
                                related_name='profile',
                                on_delete=models.CASCADE)
    wallet = models.ManyToManyField(Wallet,
                                    related_name='user')
    transaction = models.ManyToManyField(Transaction,
                                         related_name='user')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
