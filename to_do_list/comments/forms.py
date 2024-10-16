from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Form for creating and editing comments.
    This form is based on the `Comment` model and provides a user-friendly
    interface for submitting comments. Some fields are excluded from the form
    since they are managed automatically or not intended to be user-editable.
    """

    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ('author', 'active', 'object_id', 'content_type')
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Type your comment...',
                'class': 'form-control',
            }),
        }
