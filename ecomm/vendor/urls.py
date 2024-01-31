from django.urls import path

from .views import VendorList, VendorDetail, VendorLogin, VendorProfile,VendorRegistrationView


urlpatterns = [
    path('', VendorList.as_view(), name='all_vendors'),
    path('<int:uid>/', VendorDetail.as_view(), name='vendor_detail'),
    path('signin/', VendorLogin.as_view(), name='sign_in'), 
    path('register/', VendorRegistrationView.as_view(), name='vendor-register'),
    path('dashboard/', VendorProfile.as_view(), name='vendor_dashboard')

]


# urlpatterns = [
#     # ... other urlpatterns
#     path('api-token-auth/', obtain_jwt_token),
#     path('api-token-refresh/', refresh_jwt_token),
# ]