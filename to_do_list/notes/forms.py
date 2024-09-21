from django import forms
from notes.models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ('author',)