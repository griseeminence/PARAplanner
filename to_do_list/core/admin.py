from django.contrib import admin

from core.models import ParaTag


@admin.register(ParaTag)
class ParaTagAdmin(admin.ModelAdmin):
    """Admin interface configuration for the ParaTag model."""

    list_display = ('title',)
    list_filter = ('title',)
