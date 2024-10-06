from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Админка для задач."""
    list_display = ('title', 'status', 'author', 'status',)
    list_filter = ('title', 'deadline', 'author', 'status',)


# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     """Админка для тегов."""
#     list_display = ('title',)
#     list_filter = ('title',)
