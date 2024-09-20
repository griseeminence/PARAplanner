from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from para.forms import AreaForm, ProjectForm, ResourceForm
from para.models import Area, Project, Resource, ResourceType

# AREAS
# AREAS
# AREAS
# AREAS
# AREAS
# AREAS
# AREAS
# AREAS


class AreaListView(ListView):
    template_name = 'para/area_list.html'
    model = Area
    ordering = '-id'
    paginate_by = 4


class AreaDetailView(DetailView):
    template_name = 'para/area_detail.html'
    model = Area


class AreaCreateView(CreateView):
    template_name = 'para/area_create.html'
    model = Area
    success_url = reverse_lazy('para:area_list')
    form_class = AreaForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AreaUpdateView(UpdateView):
    template_name = 'para/area_create.html'
    model = Area
    form_class = AreaForm
    success_url = reverse_lazy('para:area_list')


class AreaDeleteView(DeleteView):
    template_name = 'para/area_confirm_delete.html'
    model = Area
    success_url = reverse_lazy('para:area_list')

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Area, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)




# PROJECTS
# PROJECTS
# PROJECTS
# PROJECTS
# PROJECTS
# PROJECTS


class ProjectListView(ListView):
    template_name = 'para/project_list.html'
    model = Project
    ordering = '-id'
    paginate_by = 4


class ProjectDetailView(DetailView):
    template_name = 'para/project_detail.html'
    model = Project


class ProjectCreateView(CreateView):
    template_name = 'para/project_create.html'
    model = Project
    success_url = reverse_lazy('para:project_list')
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(UpdateView):
    template_name = 'para/project_create.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('para:project_list')


class ProjectDeleteView(DeleteView):
    template_name = 'para/project_confirm_delete.html'
    model = Project
    success_url = reverse_lazy('para:project_list')

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Area, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)

# RESOURCES
# RESOURCES
# RESOURCES
# RESOURCES
# RESOURCES
# RESOURCES
# RESOURCES
# RESOURCES


class ResourceListView(ListView):
    template_name = 'para/resource_list.html'
    model = Resource
    ordering = '-id'
    paginate_by = 4


class ResourceDetailView(DetailView):
    template_name = 'para/resource_detail.html'
    model = Resource


class ResourceCreateView(CreateView):
    template_name = 'para/resource_create.html'
    model = Resource
    success_url = reverse_lazy('para:resource_list')
    form_class = ResourceForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ResourceUpdateView(UpdateView):
    template_name = 'para/resource_create.html'
    model = Resource
    form_class = ResourceForm
    success_url = reverse_lazy('para:resource_list')


class ResourceDeleteView(DeleteView):
    template_name = 'para/resource_confirm_delete.html'
    model = Resource
    success_url = reverse_lazy('para:resource_list')

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Area, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)