from django.urls import path
from .views import CreateCustomerView


urlpatterns = [
    path('register', CreateCustomerView.as_view(), name='register'),
    # path('dashboard/', CustomerProfile.as_view(), name='customer_dashboard'),
    # path('signin/', CustomerLogin.as_view(), name='sign_in')
]