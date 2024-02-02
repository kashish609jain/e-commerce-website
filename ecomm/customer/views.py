from rest_framework import generics, status
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import  CreateCustomerSerializer
from .models import Customer
class CreateCustomerView(generics.CreateAPIView):
    
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (AllowAny,)
    serializer_class =  CreateCustomerSerializer
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vendor = serializer.save()
        return Response(
            {"detail": "customer registered successfully!"},
            status=status.HTTP_201_CREATED
        )


    
      