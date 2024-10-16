from django import forms

from para.models import Area, Project, Resource


class AreaForm(forms.ModelForm):
    """
    A form for creating and updating Area instances.

    Attributes:
        new_tag (CharField): A field for entering a new tag, which is optional.
    """

    new_tag = forms.CharField(max_length=30, required=False, label="Новый тег")

    class Meta:
        model = Area
        exclude = ('author',)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'areaTitle',
                'placeholder': 'Введите заголовок'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'areaDescription',
                'placeholder': 'Описание области',
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
            })
        }

    def save(self, commit=True):
        """
        Save the Area instance to the database.
        (Using this to add different fields like tags and images)
        """

        instance = super().save(commit=False)

        if commit:
            instance.save()
            print(f"Область {instance.id} сохранена")
        return instance


class ProjectForm(forms.ModelForm):
    """
    A form for creating and updating Project instances.

    Attributes:
        new_tag (CharField): A field for entering a new tag, which is optional.
    """

    new_tag = forms.CharField(max_length=30, required=False, label="Новый тег")

    class Meta:
        model = Project
        exclude = ('author',)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'areaTitle',
                'placeholder': 'Введите заголовок'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'areaDescription',
                'placeholder': 'Описание области',
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
        }

    def save(self, commit=True):
        """
        Save the Project instance to the database.
        (Using this to add different fields like tags and images)
        """

        instance = super().save(commit=False)

        if commit:
            instance.save()
            print(f"Проект {instance.id} сохранен")
        return instance


class ResourceForm(forms.ModelForm):
    """
    A form for creating and updating Resource instances.

    Attributes:
        new_tag (CharField): A field for entering a new tag, which is optional.
    """

    new_tag = forms.CharField(max_length=30, required=False, label="Новый тег")

    class Meta:
        model = Resource
        exclude = ('author',)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'areaTitle',
                'placeholder': 'Введите заголовок'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'areaDescription',
                'placeholder': 'Описание области',
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
            'resource_type': forms.Select(attrs={
                'class': 'form-select',
                'id': 'areaStatus'
            }),
        }

    def save(self, commit=True):
        """
        Save the Resource instance to the database.
        (Using this to add different fields like tags and images)
        """

        instance = super().save(commit=False)

        if commit:
            instance.save()
            print(f"Ресурс {instance.id} сохранен")
        return instance
