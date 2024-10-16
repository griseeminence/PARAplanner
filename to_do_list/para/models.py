from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from PIL import Image

from comments.models import Comment
from core.models import ParaTag

User = get_user_model()

STATUS_CHOICES = [
    ('active', 'Active'),
    ('completed', 'Completed'),
    ('on_hold', 'On Hold'),
]

PRIORITY_CHOICES = [
    (1, 'Low'),
    (2, 'Medium'),
    (3, 'High'),
]


class BaseParaModel(models.Model):
    """
    Abstract model containing common fields for all entities (Areas, Projects, Resources,Tasks).
    """

    title = models.CharField(max_length=25, verbose_name='Title')
    description = models.TextField(max_length=1000, verbose_name='Description')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    is_archived = models.BooleanField(default=False, verbose_name='Archive')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    deadline = models.DateField(null=True, blank=True, verbose_name="Deadline")
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2, verbose_name="Priority")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    comments = GenericRelation(Comment, content_type_field='content_type', object_id_field='object_id')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='Cover Image')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Overridden method to modify the cover image before saving.
        """

        if self.cover_image:
            img = Image.open(self.cover_image.file)  # Use .file to access the file object
            img = img.resize((300, 365))
            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=85)
            thumb_file = ContentFile(thumb_io.getvalue(), name=self.cover_image.name)
            self.cover_image.save(self.cover_image.name, thumb_file, save=False)

        super().save(*args, **kwargs)


class Area(BaseParaModel):
    """
    Model representing an area that groups projects.
    """

    tags = models.ManyToManyField(ParaTag, related_name='areas', blank=True, verbose_name='Tag')

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        ordering = ('title',)

    def __str__(self):
        return f'Area: {self.title}, User: {self.author}'


class Project(BaseParaModel):
    """
    Model representing a project within a specific area.
    """
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, related_name='projects', blank=True, null=True)
    tags = models.ManyToManyField(ParaTag, related_name='projects', blank=True, verbose_name='Tag')

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ('title',)

    def __str__(self):
        return f'Project: {self.title}, User: {self.author}, Belongs to Area: {self.area}'


class Resource(BaseParaModel):
    """
    Model representing resources associated with projects and areas.
    """

    area = models.ForeignKey(Area, on_delete=models.SET_NULL, related_name='resources', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='resources', null=True, blank=True)
    tags = models.ManyToManyField(ParaTag, related_name='resources', blank=True, verbose_name='Tag')
    resource_type = models.ForeignKey('ResourceType', on_delete=models.SET_NULL, verbose_name='Resource Type',
                                      null=True, blank=True)

    class Meta:
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'
        ordering = ('title',)

    def __str__(self):
        return f'Resource: {self.title}, User: {self.author}'


class ResourceType(models.Model):
    """
    Model representing resource types.
    """

    title = models.CharField(max_length=50, unique=True, verbose_name='Тип ресурса')

    def __str__(self):
        return self.title
