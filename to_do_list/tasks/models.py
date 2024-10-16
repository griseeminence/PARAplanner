from django.contrib.auth import get_user_model
from django.db import models

from core.models import ParaTag
from para.models import BaseParaModel, Area, Resource, Project

User = get_user_model()

# Defines the various status options for a task.
STATUS_CHOICES = [
    (0, 'Pending'),
    (1, 'In Progress'),
    (2, 'Completed'),
    (3, 'Deferred'),
    (4, 'Archived'),
]


class Task(BaseParaModel):
    """
    A model representing a task within a specific project, area, and resource.
    """

    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    tags = models.ManyToManyField(ParaTag, related_name='tasks', blank=True, verbose_name='Тег')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        """
        String representation of the Task instance, displaying relevant information.
        """
        author = self.author.username if self.author else "Unknown Author"
        area = self.area if self.area else "Without Area"
        project = self.project if self.project else "Without Project"
        resource = self.resource if self.resource else "Without Resource"
        return (
            f'Task: {self.title}, '
            f'Author: {author}, '
            f'Belongs to Area: {area}, '
            f'Belongs to Project: {project}, '
            f'Belongs to Resource: {resource}'
        )
