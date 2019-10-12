from django.contrib import admin
from django.urls import path

from .views import (
    StuCreateAPIView,
    TeachCreateAPIView,
    UserLoginAPIView,
    )

urlpatterns = [
    path('register/student', StuCreateAPIView.as_view(), name='register'),
    path('register/teacher', TeachCreateAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
]