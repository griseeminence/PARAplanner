from django import forms

from core.models import ParaTag
from notes.models import Note


class NoteForm(forms.ModelForm):
    new_tag = forms.CharField(max_length=30, required=False, label="Новый тег")

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
            'new_tag': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'TagTitle',
                'placeholder': 'Введите тег'
            })
        }


    def save(self, commit=True):
        instance = super().save(commit=commit)  # Сохраняем экземпляр
        if commit:
            instance.save()  # Убедитесь, что экземпляр сохранен
        return instance
