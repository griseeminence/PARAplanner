from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('list/', views.TasksListView.as_view(), name='list'),
]



