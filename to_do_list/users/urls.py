from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView


from django.urls import include, path, reverse_lazy

from .forms import CustomUserCreationForm


urlpatterns = [
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy('core:homepage'),
        ),
        name='registration',
    ),
]
