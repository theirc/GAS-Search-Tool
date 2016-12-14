from __future__ import unicode_literals
from language_utils import LANGUAGES
from django.db import models

class Metric(models.Model):
    event = models.CharField(max_length=30)
    language = models.CharField(max_length=1, choices=LANGUAGES.items(), blank=True)
    phone = models.CharField(max_length=20)
    registration_id = models.CharField(max_length=10, blank=True)
    timestamp = models.DateField(auto_now_add=True)
