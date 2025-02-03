from django.urls import path, include
from django.urls import path
from .views import RegisterUserView, WarehouseCreateView, ProductCreateView, SupplyProductView, OrderProductView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('warehouse/', WarehouseCreateView.as_view(), name='create-warehouse'),
    path('product/', ProductCreateView.as_view(), name='create-product'),
    path('supply/', SupplyProductView.as_view(), name='supply-product'),
    path('order/', OrderProductView.as_view(), name='order-product'),
]
