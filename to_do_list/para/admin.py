from django.contrib import admin
from para.models import Area, Project, Resource, ResourceType


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    """Админка для областей."""
    list_display = (
        'title', 'description', 'created', 'is_archived', 'status', 'deadline', 'priority', 'author', 'get_tags')
    list_filter = ('title', 'created', 'author', 'status', 'is_archived', 'status', 'deadline', 'priority', 'tags')

    def get_tags(self, obj):
        """Отображает теги, связанные с областью."""
        return ", ".join([tag.title for tag in obj.tags.all()])

    get_tags.short_description = 'Теги'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Админка для проектов."""
    list_display = (
        'title', 'description', 'created', 'is_archived', 'status', 'deadline', 'priority', 'author', 'get_tags')
    list_filter = ('title', 'created', 'author', 'status', 'is_archived', 'status', 'deadline', 'priority', 'tags')

    def get_tags(self, obj):
        """Отображает теги, связанные с проектом."""
        return ", ".join([tag.title for tag in obj.tags.all()])

    get_tags.short_description = 'Теги'


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """Админка для ресурсов."""
    list_display = (
        'title', 'description', 'created', 'is_archived', 'status', 'deadline', 'priority', 'author', 'get_tags')
    list_filter = ('title', 'created', 'author', 'status', 'is_archived', 'status', 'deadline', 'priority', 'tags')

    def get_tags(self, obj):
        """Отображает теги, связанные с ресурсом."""
        return ", ".join([tag.title for tag in obj.tags.all()])

    get_tags.short_description = 'Теги'


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    """Админка для типов ресурсов."""
    list_display = ('title',)
    list_filter = ('title',)
