from django.forms import EmailField
from .exceptions import CustomException
from .models import CustomUser, Vendor
from rest_framework import serializers, generics, status
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.core.validators import EmailValidator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "uid",
            "email",
            "name",
            "password",
            "user_type",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "user_type": {"read_only": True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

# family member ke liye ?
class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    # questions ?
    # what is need of this line , agar humne model mai ek baar daldiya hai to bhi dubara specify karne ka jarurat hai ki not required ? ki fetch karne ke liye 
    master_email = serializers.EmailField(required=False)
    class Meta:
        model = Vendor
        fields = ("user", "shop_name", "phone_number", "master_email")

    def validate_master_email(self, value):
        # import ipdb; ipdb.set_trace()
        master_vendor = CustomUser.objects.filter(email=value)
        if not master_vendor.exists():
            raise ValidationError("invalid master email address")
        return value

    def create(self, validated_data):
        # import ipdb; ipdb.set_trace()
        print(validated_data)
        user_data = validated_data.pop("user")
        user_data.update({"user_type": "VENDOR"})
        master_vendor_user=CustomUser.objects.filter(email=validated_data['master_email']).first()
        user_id = master_vendor_user.uid
        user = CustomUser.objects.create_user(**user_data)
        master_vendor_id = Vendor.objects.filter(user_id = user_id).first().user.uid
        new_user = {'name': user.name, 'email': user.email}
        vendor = Vendor.objects.create(user=user,master_vendor_id = master_vendor_id, **validated_data)
        return vendor
        
class MasterVendorSerializer(serializers.ModelSerializer):
      user = UserSerializer()
    #   master_email = serializers.EmailField(required=False)
      class Meta:
        model = Vendor
        fields = ("user", "shop_name",  "phone_number")

        def create(self, validated_data):
        
            user_data = validated_data.pop("user")
            user_data.update({"user_type": "VENDOR"})
            user = CustomUser.objects.create_user(**user_data)
            user.active = False
            user.save()
            new_user =  {'name': user.name, 'email': user.email}
            vendor = Vendor.objects.create(user=user, **validated_data)
            return vendor
        

class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise CustomException({'detail':'User account does not exist'})
        
        if not user.is_confirmed:
            raise CustomException({'detail':'User account has not been confirmed'})
        elif not user.user_type == 'VENDOR':
            raise CustomException({'detail':"You are not authorized as a vendor "}, status_code=status.HTTP_401_UNAUTHORIZED)

       
        update_last_login(None, user)

        return {
            'email':user.email,
        }
