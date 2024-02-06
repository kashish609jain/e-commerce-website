from .exceptions import CustomException
from .models import CustomUser, Vendor
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "id",
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


class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    master_email = serializers.EmailField(required=False)

    class Meta:
        model = Vendor
        fields = ("user", "shop_name", "phone_number", "master_email")

    def validate_master_email(self, value):
        if value:
            master_vendor = CustomUser.objects.filter(email=value)
            if not master_vendor.exists():
                raise ValidationError("Invalid master email address")
        return value

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data.update({"user_type": "VENDOR"})
        
        master_email = validated_data.get("master_email")
        master_vendor = None

        if master_email:
            master_vendor = CustomUser.objects.filter(email=master_email).first()

        user = CustomUser.objects.create_user(**user_data)
        user.active = False
        user.save()

        if master_vendor:
            vendor = Vendor.objects.create(user=user, master_vendor_id=master_vendor.id, **validated_data)
        else:
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
        elif not user.user_type == 'VENDOR':
            raise CustomException({'detail':"You are not authorized as a customer"})

        return {
            'email':user.email
        }
