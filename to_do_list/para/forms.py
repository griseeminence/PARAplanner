from django import forms
from para.models import Area, Project, Resource


class AreaForm(forms.ModelForm):
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


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('author',)
        widgets = {
            'due_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
        }


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        exclude = ('author',)
        widgets = {
            'due_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
        }
