from django.contrib import admin

from .models import Task
from para.admin import BaseParaAdmin


@admin.register(Task)
class TaskAdmin(BaseParaAdmin):
    """Admin interface for managing Task instances."""

    pass
