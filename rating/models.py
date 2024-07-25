from django.db import models

# Create your models here.

from alice_menu.utils import BaseModel
from menu.models import Menu 
from order.models import Order

class tblRatings(BaseModel):
    date = models.CharField(max_length=20, null=True, blank=True)
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_phone = models.CharField(max_length=20, null=True, blank=True)
    outlet = models.CharField(max_length=20, null=True, blank=True)
    table_no = models.IntegerField(null=True)
    atmosphere_rating = models.FloatField()
    service_rating = models.FloatField()
    presentation_rating = models.FloatField()
    cleanliness_rating = models.FloatField()
    overall_rating = models.FloatField()
    review = models.TextField(null=True, blank=True)
    order = models.OneToOneField(Order, models.CASCADE, null=True, blank=True)

class tblitemRatings(BaseModel):
    tblrating = models.ForeignKey(tblRatings, models.CASCADE, null=True, blank=True)
    itemId = models.ForeignKey(Menu, models.CASCADE, null=True, blank=True)
    rating = models.FloatField()
    comment = models.TextField(null=True, blank=True)

# Assuming this code is in models.py or signals.py of your app

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import tblRatings





class MailRecipient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name