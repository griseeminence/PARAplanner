from django import forms

from notes.models import Note


class NoteForm(forms.ModelForm):
    """
    A form for creating and updating Note instances.

    Attributes:
        new_tag (CharField): A field for entering a new tag, which is optional.
    """

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
        """
        Save the Note instance to the database.
        (Using this to add different fields like tags and images)
        """

        instance = super().save(commit=False)

        if commit:
            instance.save()
            print(f"Заметка {instance.id} сохранена")
        return instance
