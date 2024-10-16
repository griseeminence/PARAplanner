from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin interface for managing Task instances."""

    list_display = ('title', 'status', 'author', 'status', 'get_tags')
    list_filter = ('title', 'deadline', 'author', 'status', 'tags')

    def get_tags(self, obj):
        """
        Displays the tags associated with the task.
        """
        return ", ".join([tag.title for tag in obj.tags.all()])

    get_tags.short_description = 'Tags'
