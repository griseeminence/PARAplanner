from django.contrib import admin
from core.models import ParaTag, ParaTaggedItem


@admin.register(ParaTag)
class ParaTagAdmin(admin.ModelAdmin):
    """Админка для тегов."""
    list_display = ('title',)
    list_filter = ('title',)


@admin.register(ParaTaggedItem)
class ParaTaggedItemAdmin(admin.ModelAdmin):
    """Админка для связи тегов."""
    list_display = ('tag',)
    list_filter = ('tag', 'content_type', 'object_id', 'content_object')
