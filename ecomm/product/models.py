from django.db import models
from vendor.models import Vendor, CustomUser


class Product(models.Model):
    id = models.AutoField(primary_key=True)  # Add this line to include 'id'
    name = models.CharField(max_length=200, null=True)
    quantity_available = models.PositiveIntegerField(default=0)
    price = models.FloatField()
    description = models.TextField(blank=True, null=True)
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vendor_product')

    def __str__(self):
        return self.name

class Cart(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
