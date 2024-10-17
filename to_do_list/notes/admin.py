from django.contrib import admin

from notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """
    Admin interface for the Note model.

    This class customizes the admin display for areas, showing relevant
    information such as title, description, and associated tags.
    """

    list_display = (
        'title',
        'content',
        'created',
        'area',
        'project',
        'resource',
        'author',
        'get_tags'
    )
    list_filter = (
        'title',
        'content',
        'created',
        'area',
        'project',
        'resource',
        'author',
        'tags'
    )
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-created',)
    autocomplete_fields = ['tags']
    list_per_page = 20
    readonly_fields = ('id',)
    prepopulated_fields = {'title': ('title',)}

    def get_tags(self, obj):
        """Displays the tags associated with the area."""

        return ", ".join([tag.title for tag in obj.tags.all()])

    get_tags.short_description = 'Tags'
