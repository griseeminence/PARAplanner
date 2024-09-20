from django.contrib import admin
from django.urls import include, path
from para.views import AreaCreateView, AreaDeleteView, AreaUpdateView, AreaListView, AreaDetailView

app_name = 'para'

urlpatterns = [
    path('list/', AreaListView.as_view(), name='area_list'),
    path('create/', AreaCreateView.as_view(), name='area_create'),
    path('detail/<int:pk>/', AreaDetailView.as_view(), name='area_detail'),
    path('update/<int:pk>/', AreaUpdateView.as_view(), name='area_update'),
    path('delete/<int:pk>/', AreaDeleteView.as_view(), name='area_delete'),
]
