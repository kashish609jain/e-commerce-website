from imaplib import _Authenticator
from rest_framework import generics, status
from rest_framework.generics import  CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .exceptions import CustomException
from .models import CustomUser, Vendor
from .serializers import   VendorSerializer ,UserLoginSerializer
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
class VendorRegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VendorSerializer
    def post(self, request, *args, **kwargs):
       
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Vendor registered successfully!"},
            status=status.HTTP_201_CREATED
        )
    
class VendorLoginView(CreateAPIView):
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

class VendorLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()

        return Response({"success": "Logout successful"}, status=status.HTTP_200_OK)

class VendorList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Vendor.objects.all()
        serializer = VendorSerializer(queryset, many=True)
        return Response(serializer.data)    