from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
# from django.contrib.auth import user


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class TodoDetail(models.Model):
	user = models.ForeignKey(User, related_name='todo_detail')
	todo = models.CharField(max_length=100)
	STATUS_CHOICES = ((1, 'Open'), (2, 'In-Progress'), (3, 'Resolved'), (4, 'Closed'))
	status = models.IntegerField(choices=STATUS_CHOICES,default=1)
	tag = models.ManyToManyField(TagDetail)

class TagDetail(models.Model):
	tag = models.CharField(max_length=50)
