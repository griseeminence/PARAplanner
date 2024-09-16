from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('author',)
        widgets = {
            'due_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            )
        }