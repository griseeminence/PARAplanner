from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface for the Comment model.

    This class customizes the admin display for areas, showing relevant
    information such as title, description.
    """
    list_display = ('text', 'created', 'author', 'updated', 'active')
    list_filter = ('created', 'author', 'updated', 'active',)
