from vendor.exceptions import CustomException
from vendor.models import CustomUser
from vendor.serializers import UserSerializer
from rest_framework import serializers, generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ("user", "address", "city", "state", "phone_number")


    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_data.update({"user_type": "CUSTOMER"})
        user = CustomUser.objects.create_user(**user_data)
        user.active = False
        user.save()
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise CustomException({'detail':'User account does not exist'})
        elif not user.user_type == 'CUSTOMER':
            raise CustomException({'detail':"You are not authorized as a customer"}, status_code=status.HTTP_401_UNAUTHORIZED)

        update_last_login(None, user)

        return {
            'email':user.email
        }

    