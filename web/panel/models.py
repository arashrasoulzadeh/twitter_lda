# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class TwitterUsers(models.Model):
    username = models.CharField(max_length=50,unique=True)


class TwitterPost(models.Model):
    user = models.ForeignKey(TwitterUsers)
    text = models.CharField(max_length=144)
    date = models.DateTimeField()
