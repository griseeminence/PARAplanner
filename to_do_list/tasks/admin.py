from django.contrib import admin
from .models import Task


@admin.register(Task)
class IngredientAdmin(admin.ModelAdmin):
    """Админка для ингредиентов."""
    list_display = ('title', 'status', 'author', 'status',)
    list_filter = ('title', 'due_date', 'author', 'status',)
