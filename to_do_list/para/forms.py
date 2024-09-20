from django import forms
from para.models import Area, Project, Resource


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        exclude = ('author',)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('author',)


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        exclude = ('author',)