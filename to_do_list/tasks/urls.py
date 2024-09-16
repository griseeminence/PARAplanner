from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('list/', views.TaskListView.as_view(), name='list'),
    path('create/', views.TaskCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.TaskUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.TaskDeleteView.as_view(), name='delete'),
    path('detail/<int:pk>/', views.TaskDetailView.as_view(), name='detail'),
]
