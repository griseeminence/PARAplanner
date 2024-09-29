from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ('author', 'active', 'object_id', 'content_type')
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Напишите комментарий...',
                'class': 'form-control',
            }),
        }
