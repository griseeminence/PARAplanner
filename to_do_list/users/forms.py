from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form that extends the default UserCreationForm."""
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')
