from django.contrib import admin
from para.models import Area, Project, Resource, ResourceType


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    """
    Admin interface for the Area model.

    This class customizes the admin display for areas, showing relevant
    information such as title, description, and associated tags.
    """

    list_display = (
        'title', 'description', 'created', 'is_archived', 'status', 'deadline', 'priority', 'author', 'get_tags')
    list_filter = ('title', 'created', 'author', 'status', 'is_archived', 'status', 'deadline', 'priority', 'tags')

    def get_tags(self, obj):
        """
        Displays the tags associated with the area.
        """

        return ", ".join([tag.title for tag in obj.tags.all()])

    get_tags.short_description = 'Tags'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin interface for the Project model.

    This class customizes the admin display for areas, showing relevant
    information such as title, description, and associated tags.
    """

    list_display = (
        'title', 'description', 'created', 'is_archived', 'status', 'deadline', 'priority', 'author', 'get_tags')
    list_filter = ('title', 'created', 'author', 'status', 'is_archived', 'status', 'deadline', 'priority', 'tags')

    def get_tags(self, obj):
        """
        Displays the tags associated with the project.
        """
        return ", ".join([tag.title for tag in obj.tags.all()])

    get_tags.short_description = 'Tags'


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """
    Admin interface for the Resource model.

    This class customizes the admin display for areas, showing relevant
    information such as title, description, and associated tags.
    """

    list_display = (
        'title', 'description', 'created', 'is_archived', 'status', 'deadline', 'priority', 'author', 'get_tags')
    list_filter = ('title', 'created', 'author', 'status', 'is_archived', 'status', 'deadline', 'priority', 'tags')

    def get_tags(self, obj):
        """
        Displays the tags associated with the resource.
        """
        return ", ".join([tag.title for tag in obj.tags.all()])

    get_tags.short_description = 'Tags'


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    """
    Admin interface for the ResourceType model.
    This class customizes the admin display for resource types, allowing
    for straightforward management of resource categories.
    """

    list_display = ('title',)
    list_filter = ('title',)
