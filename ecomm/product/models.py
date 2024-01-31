from django.db import models
from vendor.models import Vendor


class Category(models.Model):
    name = models.CharField(max_length=200) 
    class Meta:
        ordering = ('name',) # Specifies the default sorting order for querysets of this model. In this case, it orders by the name field in ascending order .
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    categories = models.ManyToManyField(Category, related_name='categories')
    quantity_available = models.PositiveIntegerField(default=0)
    price = models.FloatField()
    description = models.TextField(blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor')

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(unique=True)

    def __str__(self):
        return f"{self.image.url}"
    
