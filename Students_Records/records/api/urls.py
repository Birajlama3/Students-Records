from django.urls import path, include
from rest_framework import routers

urlpatterns = [
    path('',include(routers.urls)),
    path('api-auth/',include("rest_framework.urls", namespace="rest_framework")),
]
