from io import BytesIO
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image

from comments.models import Comment
from core.models import ParaTag
from para.models import Area, Project, Resource

User = get_user_model()


class Note(models.Model):
    """
    The Note model represents a note associated with areas, projects, and resources
    within the PARA project. Each note contains a title, content, and optional
    tags and cover images. Notes can be associated with a specific area, project,
    or resource and can be archived.
    """

    title = models.CharField(max_length=100, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    is_archived = models.BooleanField(default=False, verbose_name='Archive')
    comments = GenericRelation(Comment, content_type_field='content_type', object_id_field='object_id')
    tags = models.ManyToManyField(ParaTag, related_name='notes', blank=True, verbose_name='Tag')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='Cover Image')

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        ordering = ('created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """"
        Saves the note instance, processing the cover image if it exists.
        """

        if self.cover_image:
            img = Image.open(self.cover_image.file)  # Access the file object
            img = img.resize((300, 365))
            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=85)
            thumb_file = ContentFile(thumb_io.getvalue(), name=self.cover_image.name)
            self.cover_image.save(self.cover_image.name, thumb_file, save=False)

        super().save(*args, **kwargs)
