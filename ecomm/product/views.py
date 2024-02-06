# views.py
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import serializers
from .models import Product
from .serializers import ProductSerializer
from vendor.models import Vendor, CustomUser
from rest_framework.permissions import IsAuthenticated
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['product', 'quantity']

class CreateListProduct(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get(self, request, user_id=None):

        if user_id:
            vendor = get_object_or_404(CustomUser, id=user_id)
            products = Product.objects.filter(vendor=vendor)
        else:
            products = Product.objects.all()

        data = ProductSerializer(products, many=True).data
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vendor = get_object_or_404(Vendor, user=request.user)
        product = Product.objects.create(vendor=vendor.user,
        name=serializer.data['name'],
        price=serializer.data['price'],
        quantity_available=serializer.data['quantity_available'],
        description=serializer.data['description'])

        return Response(
            {"detail": "Product successfully created!"}, status=status.HTTP_201_CREATED
        )

class AddToCartView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        customer = get_object_or_404(CustomUser, id=self.request.user.id)
        serializer.save(customer=customer, product=serializer.validated_data['product'])

class CartListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        customer = get_object_or_404(CustomUser, id=self.request.user.id)
        return Cart.objects.filter(customer=customer)
