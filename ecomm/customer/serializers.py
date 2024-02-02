from rest_framework import serializers, generics, status
from vendor.models import CustomUser
from vendor.serializers import UserSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from .models import Customer


class CreateCustomerSerializer(serializers.ModelSerializer):
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


