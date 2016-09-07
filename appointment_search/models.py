from django.conf import settings
from django.db import models


class AsylumOffice(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class AsylumOfficeDetails(models.Model):
    office = models.ForeignKey(AsylumOffice, null=True, blank=True)
    language = models.CharField(max_length=10, null=True, blank=True, choices=getattr(settings, 'LANGUAGES', None))
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class AppointmentSchedule(models.Model):
    registration_number = models.CharField(max_length=100, null=True, blank=True)
    office = models.ForeignKey(AsylumOffice, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.registration_number
