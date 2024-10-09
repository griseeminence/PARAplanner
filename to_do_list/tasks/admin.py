from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Админка для задач."""
    list_display = ('title', 'status', 'author', 'status', 'get_tags')
    list_filter = ('title', 'deadline', 'author', 'status', 'tags')

    def get_tags(self, obj):
        """Отображает теги, связанные с задачей."""
        return ", ".join([tag.title for tag in obj.tags.all()])
    get_tags.short_description = 'Теги'

# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     """Админка для тегов."""
#     list_display = ('title',)
#     list_filter = ('title',)
