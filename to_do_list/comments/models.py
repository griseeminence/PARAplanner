from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Comment(models.Model):
    """
    Model representing a comment associated with various content types.
    This model allows users to leave comments on different models through
    Django's GenericForeignKey mechanism. It stores the comment's content,
    author, timestamps, and its relation to a specific content type.
    """

    text = models.TextField(max_length=2000, blank=True, null=True, verbose_name='Text')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated')
    active = models.BooleanField(default=True, verbose_name='Active')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Content Type'
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('-created',)

    def __str__(self):
        return (
            f"Commented by: {self.author}"
            f"Created: {self.created}"
        )
