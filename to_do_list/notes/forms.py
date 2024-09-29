from django import forms
from notes.models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ('author',)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'areaTitle',
                'placeholder': 'Введите заголовок'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'areaDescription',
                'placeholder': 'Описание области',
                'rows': 5
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