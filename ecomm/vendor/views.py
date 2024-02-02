from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import CustomUser, Vendor
from .serializers import  VendorSerializer, UserLoginSerializer, VendorDashboardSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class VendorDashboardView(generics.RetrieveDestroyAPIView, generics.CreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = VendorDashboardSerializer
    def get_object(self):
        # Ensure that the user can only access their own dashboard
        user = self.request.user
        vendor = get_object_or_404(Vendor, user=user)
        self.check_object_permissions(self.request, vendor)
        return vendor
    
    def get(self, request, *args, **kwargs):
        return Response("dashboard")

    def delete(self, request, *args, **kwargs):
        return Response("delete")
    
    def post(self, request, *args, **kwargs):
        return Response("add")

class VendorRegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VendorSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vendor = serializer.save()
        return Response(
            {"detail": "Vendor registered successfully!"},
            status=status.HTTP_201_CREATED
        )

class VendorLogin(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer  # Use UserLoginSerializer for data validation
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = CustomUser.objects.filter(email=email).first()

        if user:
            user_id = user.id
            dashboard_url = reverse('vendor-dashboard', kwargs={'id': user_id})
            return Response({"success": "Login successful", "redirect_url": dashboard_url})
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED) 
    
class VendorList(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)  
    queryset = Vendor.objects.all()  
    serializer_class = VendorSerializer  


# Define a view for retrieving details of a vendor
# class VendorDetail(generics.RetrieveAPIView):
#     permission_classes = (AllowAny,)  # Allow any user to access this view
#     queryset = Vendor.objects.all()  # Retrieve all Vendor instances from the database
#     serializer_class = VendorSerializer  # Use VendorSerializer for serialization

# Define a view for user login
    
# Define a view for retrieving a vendor profile
# class VendorProfile(RetrieveAPIView):
#     permission_classes = (IsVendor,)  # Require authentication and vendor permission to access this view
#     # authentication_class = JSONWebTokenAuthentication  # Use JWT authentication

#     def get(self, request):
#         vendor = get_object_or_404(Vendor, user=request.user)  # Retrieve the vendor instance associated with the authenticated user
#         data = VendorSerializer(vendor).data  # Serialize the vendor data
#         return Response(data, status=status.HTTP_200_OK)

# class VendorLogin(CreateAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = UserLoginSerializer  # Use UserLoginSerializer for data validation

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)  # Create a serializer instance with request data
#         serializer.is_valid(raise_exception=True)  # Validate the data, raise an exception if invalid
#         response = {
#             'success' : 'True',
#             'status code' : status.HTTP_200_OK,
#             'message': 'User logged in successfully',
#         }
#         status_code = status.HTTP_200_OK

#         return Response(response, status=status_code)

# def dashboard(request, uid):
#     try:
#         # Assuming Vendor is your model and 'uid' is a field in Vendor
#         vendor = Vendor.objects.get(uid=uid)

#         # Your logic for retrieving additional details about the vendor
#         # For example, assuming you have fields 'name' and 'email' in the Vendor model
#         vendor_name = vendor.name
#         vendor_email = vendor.email

#         # Render the vendor_dashboard.html template with vendor details
#         context = {
#             'vendor_name': vendor_name,
#             'vendor_email': vendor_email,
#             # Add more fields as needed
#         }

#         return HttpResponse("Vendor found", status=200)
#     except Vendor.DoesNotExist:
#         return HttpResponse("Vendor not found", status=404)

# Define a view for vendor registration
# class VendorRegistrationView(generics.CreateAPIView):
#     permission_classes = (AllowAny,)  # Allow any user to access this view
#     serializer_class = VendorSerializer  # Use VendorSerializer for data validation

#     def post(self, request, *args, **kwargs):
#         # import ipdb; ipdb.set_trace()
#         print(request.data)
#         serializer = self.get_serializer(data=request.data)  # Create a serializer instance with request data
#         serializer.is_valid(raise_exception=True)  # Validate the data, raise an exception if invalid
#         vendor = serializer.save()  # Save the validated data to create a new Vendor instance

#         # Additional logic for vendor registration if needed
     
#         return Response(
#             {"detail": "Vendor registered successfully!"},
#             status=status.HTTP_201_CREATED
#         ) 
# class MasterVendorRegistrationView(generics.CreateAPIView):
#     permission_classes = (AllowAny,)  # Allow any user to access this view
#     serializer_class = MasterVendorSerializer # Use VendorSerializer for data validation

#     def post(self, request, *args, **kwargs):
#         # import ipdb; ipdb.set_trace()
#         print(request.data)
#         serializer = self.get_serializer(data=request.data)  # Create a serializer instance with request data
#         serializer.is_valid(raise_exception=True)  # Validate the data, raise an exception if invalid
#         vendor = serializer.save()  # Save the validated data to create a new Vendor instance

#         # Additional logic for vendor registration if needed
     
#         return Response(
#             {"detail": "Vendor registered successfully!"},
#             status=status.HTTP_201_CREATED
#         )     

# def vendor_dashboard(request, uid):
#     try:
#         return HttpResponse("vendor found")
#     except Vendor.DoesNotExist:
#         return HttpResponse("Vendor not found", status=404)
    
# class VendorDashboardGet(RetrieveAPIView,CreateAPIView,):
#     serializer_class = VendorProductSerializer

#     def get(self, request, *args, **kwargs):
#         return Response("all products displayed")
  
 
# class VendorDashboardPost(CreateAPIView):
      