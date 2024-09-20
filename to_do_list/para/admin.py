from django.contrib import admin
from para.models import Area, Project, Resource, ResourceType


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    """Админка для областей."""
    list_display = ('title', 'description', 'created', 'is_archived', 'status', 'deadline', 'priority', 'author')
    list_filter = ('title', 'created', 'author', 'status', 'is_archived', 'status', 'deadline', 'priority',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Админка для проектов."""
    list_display = ('title', 'description', 'created', 'is_archived', 'status', 'deadline', 'priority', 'author')
    list_filter = ('title', 'created', 'author', 'status', 'is_archived', 'status', 'deadline', 'priority',)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """Админка для ресурсов."""
    list_display = ('title', 'description', 'created', 'is_archived', 'status', 'deadline', 'priority', 'author')
    list_filter = ('title', 'created', 'author', 'status', 'is_archived', 'status', 'deadline', 'priority',)


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    """Админка для типов ресурсов."""
    list_display = ('title',)
    list_filter = ('title',)
