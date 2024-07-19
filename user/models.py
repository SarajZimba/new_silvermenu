import datetime
import random
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from alice_menu.utils import BaseModel

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class Customer(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=False)
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    phone = models.CharField(max_length=255, null=True, blank=False)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=False)
    type = models.CharField(max_length=255, null=True, blank=False)
    cardNo = models.CharField(max_length=255, null=True, blank=False)
    phone = models.CharField(max_length=255, null=True, blank=True)
    vatNo = models.CharField(max_length=255, null=True, blank=False)


    def __str__(self):
        return f"{self.full_name} - ({self.email})"

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = f"{self.username}@silverlinepos.com"
        super().save(*args, **kwargs)

class CustomerNormalLoginManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        
        user = self.model(username=username, **extra_fields)
        if password is not None:
            user.set_password(password)
        user.save(using=self._db)
        return user
    
class CustomerNormalLogin(AbstractBaseUser):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    email = models.CharField(max_length=255, null=True)
    reset_token = models.CharField(max_length = 1000, default=uuid.uuid4, editable=False)
    reset_token_expiry = models.DateTimeField(null=True, blank=True)

    objects = CustomerNormalLoginManager()

    def __str__(self):
        return self.username
    
# class CustomerGooglelogin(BaseModel):
#     customer = models.ForeignKey(Customer, models.SET_NULL, null=True)
#     email = models.CharField(max_length=255, null=True)
#     google_id = models.CharField(max_length=200, null=True)
#     def __str__(self):
#         return f"{self.customer.name}"

class CustomerGoogleLoginManager(BaseUserManager):
    def create_user(self, username, google_id=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        
        user = self.model(username=username, **extra_fields)
        if google_id is not None:
            user.set_password(google_id)
        user.save(using=self._db)
        return user

class CustomerGoogleLogin(AbstractBaseUser):
    customer = models.ForeignKey(Customer, models.SET_NULL, null=True)
    email = models.CharField(max_length=255, null=True)
    google_id = models.CharField(max_length=200, null=True)
    def __str__(self):
        return f"{self.customer.name}"
    
class UserLogin(BaseModel):
    device_token = models.CharField(max_length=355)
    outlet = models.CharField(max_length=100)



import datetime
import random
import uuid

from django.contrib.auth.models import AbstractUser

from django.db import models




class User(AbstractBaseUser, BaseModel):
    full_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    image = models.ImageField(upload_to="user/images/", null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} - ({self.email})"

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = f"{self.username}@silverlinepos.com"
        super().save(*args, **kwargs)