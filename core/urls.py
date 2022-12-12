from django.urls import path 
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('productslist/', ProductsList.as_view(), name='productslist'),
    path('product/<str:pk>',ProductView.as_view(), name='product'),
    path('oreder/', OrederView.as_view(), name="oreder"),
    path('orederupdate/', EditOrederView.as_view(), name='orederupdate'),
    path('removeitem/<str:pk>', DeleteItemView.as_view(), name='removeitem'),
    path('address/', AddressView.as_view(), name='address'),
  
    
]