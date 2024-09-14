from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
]
