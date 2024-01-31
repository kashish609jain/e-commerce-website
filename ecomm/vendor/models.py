from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("email address cannot be left empty!"))
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
            raise ValueError(_("superuser must set is_staff to True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("superuser must set is_superuser to True"))

        return self.create_user(email, password, **extra_fields)

        

class CustomUser(AbstractUser):
 
    # Translatable string
    USER_TYPE_CHOICES = (
      ('VENDOR', 'Vendor'),
      ('CUSTOMER', 'Customer'),
      ('ADMIN', 'Administrator')
    )

    username = None
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), blank=False, unique=True)
    name = models.CharField(_("name"), max_length=150, blank=False)
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=15)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email



#The Vendor model extends the CustomUser model through a one-to-one relationship.
# It means that each instance of the Vendor model is associated with exactly one instance of the CustomUser model.
#CustomUser: This is the model with which the one-to-one relationship is established. In this case, each Vendor is associated with a single CustomUser.
#on_delete=models.CASCADE: This argument specifies what should happen when the referenced CustomUser instance is deleted. In this case, CASCADE is used, which means that if a CustomUser is deleted, the associated Vendor will also be deleted. This is a common choice for a one-to-one relationship, as it ensures referential integrity.        
class Vendor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    shop_name = models.CharField(_("shop name"), blank=False, null=False, max_length=250
    )
    phone_number = models.CharField(
        _("phone number"), blank=False, null=False, max_length=11
    )

    def __str__(self):
        return self.shop_name
    