from django.contrib import admin
from .router import router
from django.urls import include, path



urlpatterns = [
    path('', include(router.urls))
    ]
