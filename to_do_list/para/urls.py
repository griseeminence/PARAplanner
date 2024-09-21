from django.contrib import admin
from django.urls import include, path
from para.views import *

app_name = 'para'

urlpatterns = [
    path('area/list/', AreaListView.as_view(), name='area_list'),
    path('area/create/', AreaCreateView.as_view(), name='area_create'),
    path('area/detail/<int:pk>/', AreaDetailView.as_view(), name='area_detail'),
    path('area/update/<int:pk>/', AreaUpdateView.as_view(), name='area_update'),
    path('area/delete/<int:pk>/', AreaDeleteView.as_view(), name='area_delete'),
    path('project/list/', ProjectListView.as_view(), name='project_list'),
    path('project/create/', ProjectCreateView.as_view(), name='project_create'),
    path('project/detail/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('project/update/<int:pk>/', ProjectUpdateView.as_view(), name='project_update'),
    path('project/delete/<int:pk>/', ProjectDeleteView.as_view(), name='project_delete'),
    path('resource/list/', ResourceListView.as_view(), name='resource_list'),
    path('resource/create/', ResourceCreateView.as_view(), name='resource_create'),
    path('resource/detail/<int:pk>/', ResourceDetailView.as_view(), name='resource_detail'),
    path('resource/update/<int:pk>/', ResourceUpdateView.as_view(), name='resource_update'),
    path('resource/delete/<int:pk>/', ResourceDeleteView.as_view(), name='resource_delete'),
    path('dashboard/', DashBoardView.as_view(), name='dashboard'),
]
