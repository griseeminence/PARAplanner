from django.contrib import admin
from core.models import ParaTag


@admin.register(ParaTag)
class ParaTagAdmin(admin.ModelAdmin):
    """Админка для тегов."""
    list_display = ('title',)
    list_filter = ('title',)


