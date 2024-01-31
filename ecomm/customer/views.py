#API VIews
from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView, CreateAPIView

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from vendor.models import CustomUser
from .models import Customer
from .permissions import IsCustomer
from .serializers import CustomerSerializer, UserLoginSerializer


# List and Create customers
class CreateCustomer(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# Get details of a vendor
class CustomerProfile(generics.RetrieveAPIView):
    permission_classes = (IsCustomer,)
   
    def get(self, request):
        customer = get_object_or_404(Customer, user=request.user)
        data = CustomerSerializer(customer).data
        return Response(data, status=status.HTTP_200_OK)


#Login User
class CustomerLogin(CreateAPIView):

    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)
