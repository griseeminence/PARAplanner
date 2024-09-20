from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class TagAdmin(admin.ModelAdmin):
    """Админка для тегов."""
    list_display = ('text', 'created', 'author', 'updated', 'active', 'task')
    list_filter = ('created', 'author', 'updated', 'active', 'task')

