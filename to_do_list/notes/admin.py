from django.contrib import admin
from notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Админка для заметок."""
    list_display = ('title', 'content', 'created', 'area', 'project', 'resource', 'author',)
    list_filter = ('title', 'content', 'created', 'area', 'project', 'resource', 'author',)
