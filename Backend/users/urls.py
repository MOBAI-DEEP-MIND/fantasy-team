from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from django.urls import path
from .views import Signup

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/',Signup.as_view(),name='signup'),
]