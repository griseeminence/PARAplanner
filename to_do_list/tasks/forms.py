from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    """
    A form for creating and updating Task instances.

    Attributes:
        new_tag (CharField): A field for entering a new tag, which is optional.
    """

    new_tag = forms.CharField(max_length=30, required=False, label="New Tag")

    class Meta:
        model = Task
        exclude = ('author',)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'areaTitle',
                'placeholder': 'Enter title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'areaDescription',
                'placeholder': 'Area description',
                'rows': 5
            }),
            'deadline': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control',
                'id': 'areaDeadline',
                'type': 'date'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
                'id': 'areaPriority'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'id': 'areaStatus'
            }),
            'is_archived': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'type': 'checkbox',
                'id': 'loginCheck',
            }),
            'area': forms.Select(attrs={
                'class': 'form-select',
                'id': 'areaStatus'
            }),
            'project': forms.Select(attrs={
                'class': 'form-select',
                'id': 'areaStatus'
            }),
            'resource': forms.Select(attrs={
                'class': 'form-select',
                'id': 'areaStatus'
            }),
        }

    def save(self, commit=True):
        """
        Save the Task instance to the database.
        (Using this to add different fields like tags and images)
        """

        instance = super().save(commit=False)

        if commit:
            instance.save()
            print(f"Задача {instance.id} сохранена")
        return instance
