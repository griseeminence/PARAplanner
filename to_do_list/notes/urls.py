from django.urls import path

from notes.views import *

app_name = 'notes'

urlpatterns = [
    path('note/list/', NoteListView.as_view(), name='note_list'),
    path('note/create/', NoteCreateView.as_view(), name='note_create'),
    path('note/detail/<int:pk>/', NoteDetailView.as_view(), name='note_detail'),
    path('note/update/<int:pk>/', NoteUpdateView.as_view(), name='note_update'),
    path('note/delete/<int:pk>/', NoteDeleteView.as_view(), name='note_delete'),
]
