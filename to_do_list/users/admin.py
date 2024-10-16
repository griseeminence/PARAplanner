from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    """Admin interface for managing User instances."""
    list_filter = ('email', 'first_name')
    list_display = (
        'email',
        'first_name',
        'last_name',
        'id',
        'username',
    )
