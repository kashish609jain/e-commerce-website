# Import necessary modules and classes
from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView, CreateAPIView

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

# Import models, permissions, and serializers from the application
from .models import CustomUser, Vendor
from .permissions import IsVendor
from .serializers import  VendorSerializer, UserLoginSerializer, MasterVendorSerializer

# Define a view for vendor registration
class VendorRegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)  # Allow any user to access this view
    serializer_class = VendorSerializer  # Use VendorSerializer for data validation

    def post(self, request, *args, **kwargs):
        # import ipdb; ipdb.set_trace()
        print(request.data)
        serializer = self.get_serializer(data=request.data)  # Create a serializer instance with request data
        serializer.is_valid(raise_exception=True)  # Validate the data, raise an exception if invalid
        vendor = serializer.save()  # Save the validated data to create a new Vendor instance

        # Additional logic for vendor registration if needed
     
        return Response(
            {"detail": "Vendor registered successfully!"},
            status=status.HTTP_201_CREATED
        ) 
class MasterVendorRegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)  # Allow any user to access this view
    serializer_class = MasterVendorSerializer # Use VendorSerializer for data validation

    def post(self, request, *args, **kwargs):
        # import ipdb; ipdb.set_trace()
        print(request.data)
        serializer = self.get_serializer(data=request.data)  # Create a serializer instance with request data
        serializer.is_valid(raise_exception=True)  # Validate the data, raise an exception if invalid
        vendor = serializer.save()  # Save the validated data to create a new Vendor instance

        # Additional logic for vendor registration if needed
     
        return Response(
            {"detail": "Vendor registered successfully!"},
            status=status.HTTP_201_CREATED
        )     


# Define a view for listing and creating vendors
class VendorList(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)  # Allow any user to access this view
    queryset = Vendor.objects.all()  # Retrieve all Vendor instances from the database
    serializer_class = VendorSerializer  # Use VendorSerializer for serialization

# Define a view for retrieving details of a vendor
class VendorDetail(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)  # Allow any user to access this view
    queryset = Vendor.objects.all()  # Retrieve all Vendor instances from the database
    serializer_class = VendorSerializer  # Use VendorSerializer for serialization


# Define a view for user login
class VendorLogin(CreateAPIView):
    serializer_class = UserLoginSerializer  # Use UserLoginSerializer for data validation

    def post(self, request):
        serializer = self.serializer_class(data=request.data)  # Create a serializer instance with request data
        serializer.is_valid(raise_exception=True)  # Validate the data, raise an exception if invalid
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in successfully',
            'token' : serializer.data['token'],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

# Define a view for retrieving a vendor profile
class VendorProfile(RetrieveAPIView):
    permission_classes = (IsVendor,)  # Require authentication and vendor permission to access this view
    # authentication_class = JSONWebTokenAuthentication  # Use JWT authentication

    def get(self, request):
        vendor = get_object_or_404(Vendor, user=request.user)  # Retrieve the vendor instance associated with the authenticated user
        data = VendorSerializer(vendor).data  # Serialize the vendor data
        return Response(data, status=status.HTTP_200_OK)
