from django.contrib import admin
from notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Админка для заметок."""
    list_display = ('title', 'content', 'created', 'area', 'project', 'resource', 'author', 'get_tags')
    list_filter = ('title', 'content', 'created', 'area', 'project', 'resource', 'author', 'tags')

    def get_tags(self, obj):
        """Отображает теги, связанные с заметкой."""
        return ", ".join([tag.title for tag in obj.tags.all()])
    get_tags.short_description = 'Теги'