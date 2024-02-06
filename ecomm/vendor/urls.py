from django.urls import path
from .views import VendorRegistrationView, VendorLoginView , VendorLogoutView ,VendorList

urlpatterns = [
    path('register/', VendorRegistrationView.as_view(), name='vendor-register'),
    path('signin/',VendorLoginView.as_view(),name='vendor-signin'),
    path('logout/', VendorLogoutView.as_view(), name='vendor-logout'),
    path('',VendorList.as_view(),name ='vendor-list')
]
