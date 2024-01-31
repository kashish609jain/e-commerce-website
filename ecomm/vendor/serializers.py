from .exceptions import CustomException
from .models import CustomUser, Vendor
from rest_framework import serializers, generics, status

from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login



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


class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Vendor
        fields = ("user", "shop_name", "phone_number", )

       
    def create(self, validated_data):
        
        user_data = validated_data.pop("user")
        user_data.update({"user_type": "VENDOR"})
        user = CustomUser.objects.create_user(**user_data)
        user.active = False
        user.save()
        
        new_user = {'name':user.name, 'email':user.email}
    
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
