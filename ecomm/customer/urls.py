from django.urls import path
from .views import CreateCustomerView,CustomerLoginView,CustomerLogoutView,CustomerList


urlpatterns = [
    path('register', CreateCustomerView.as_view(), name='register'),
    path('signin/', CustomerLoginView.as_view(), name='sign_in'),
    path('logout/',CustomerLogoutView.as_view(),name = 'customer_logout'),
    path('',CustomerList.as_view(),name = 'customer-list')
]