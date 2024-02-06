from django.urls import path
from .views import AddToCartView, CartListView, CreateListProduct

urlpatterns = [
    path('', CreateListProduct.as_view(), name='create_list_products'),
    path('<int:user_id>/', CreateListProduct.as_view(), name='get_vendor_products'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', CartListView.as_view(), name='cart-list'),
   
]


