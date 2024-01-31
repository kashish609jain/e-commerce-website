from django.urls import path

from .views import CustomerLogin

from .views import CreateCustomer, CustomerProfile


urlpatterns = [
    path('', CreateCustomer.as_view(), name='all_vendors'),
    path('dashboard/', CustomerProfile.as_view(), name='customer_dashboard'),
    path('signin/', CustomerLogin.as_view(), name='sign_in'),
    
]