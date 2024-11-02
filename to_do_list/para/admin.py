from django.contrib import admin
from para.models import Area, Project, Resource, ResourceType


class BaseParaAdmin(admin.ModelAdmin):
    """Base admin configuration for models with similar admin behavior."""

    list_display = (
        'title',
        'description',
        'created',
        'is_archived',
        'status',
        'deadline',
        'priority',
        'author',
        'get_tags'
    )
    list_filter = (
        'title',
        'created',
        'author',
        'status',
        'is_archived',
        'deadline',
        'priority',
        'tags'
    )
    search_fields = ('title', 'description', 'author__username')
    ordering = ('-created', 'priority', 'deadline')
    autocomplete_fields = ['tags']
    date_hierarchy = 'created'
    list_per_page = 20
    readonly_fields = ('id',)
    prepopulated_fields = {'title': ('title',)}

    def get_tags(self, obj):
        """Retrieve and display related tags as a comma-separated string."""

        return ", ".join([tag.title for tag in obj.tags.all()])

    get_tags.short_description = 'Tags'


# Наследуемся от базового класса для конкретных моделей

@admin.register(Area)
class AreaAdmin(BaseParaAdmin):
    """Admin configuration for the Area model."""

    pass


@admin.register(Project)
class ProjectAdmin(BaseParaAdmin):
    """Admin configuration for the Project model."""

    pass


@admin.register(Resource)
class ResourceAdmin(BaseParaAdmin):
    """Admin configuration for the Resource model."""
    pass


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    """
    Admin interface for the ResourceType model.
    This class customizes the admin display for resource types, allowing
    for straightforward management of resource categories.
    """

    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ('title',)
    ordering = ('title',)
