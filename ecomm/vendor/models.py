from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("email address cannot be left empty!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("user_type", 'ADMIN')

        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser must set is_staff to True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser must set is_superuser to True")

        return self.create_user(email, password, **extra_fields)

        

class CustomUser(AbstractUser):
 
   
    USER_TYPE_CHOICES = (
      ('VENDOR', 'Vendor'),
      ('CUSTOMER', 'Customer'),
      ('ADMIN', 'Administrator')
    )

    username = None
    id = models.AutoField(primary_key=True)
    email = models.EmailField(blank=False, unique=True)
    name = models.CharField(max_length=150, blank=False)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=15,null=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    
class Vendor(models.Model):

    def is_vendor(self):
        return self.user.email if self.user else None
    
    user = models.OneToOneField("vendor.CustomUser", on_delete=models.CASCADE, primary_key=True)
    shop_name = models.CharField( blank=False, null=False, max_length=250)
    phone_number = models.CharField(blank=False, null=False, max_length=11)
    master_email = models.EmailField(blank=True, null=True)
    master_vendor = models.ForeignKey("vendor.Vendor", null=True, on_delete=models.SET_NULL)
    
    
   
    
