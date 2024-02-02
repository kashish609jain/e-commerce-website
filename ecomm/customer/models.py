from django.db import models
from vendor.models import CustomUser


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(blank=False, null=False, max_length=250)
    city = models.CharField(blank=False, null=False, max_length=20)
    state = models.CharField(blank=False, null=False, max_length=250)
    phone_number = models.CharField(blank=False, null=False, max_length=11)

    def __str__(self):
        return self.user.email