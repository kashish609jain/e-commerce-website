from rest_framework import generics, status
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from  vendor.exceptions import CustomException
from .serializers import  CreateCustomerSerializer,UserLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import Customer
class CreateCustomerView(generics.CreateAPIView):
    
    
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

#Login User
class CustomerLoginView(generics.CreateAPIView):
    
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except CustomException as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        email = serializer.validated_data.get('email')
        user = authenticate(request=request, email=email, password=request.data.get('password'))

        if user:
            # Create or retrieve a token for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "success": "Login successful"})
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class CustomerLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()

        return Response({"success": "Logout successful"}, status=status.HTTP_200_OK)

class CustomerList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Customer.objects.all()
        serializer = CreateCustomerSerializer(queryset, many=True)
        return Response(serializer.data)        

class CustomerLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()

        return Response({"success": "Logout successful"}, status=status.HTTP_200_OK)

 