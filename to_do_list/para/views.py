from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse

from notes.models import Note
from para.forms import AreaForm, ProjectForm, ResourceForm
from para.models import Area, Project, Resource, ResourceType
from tasks.models import Task

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

    def get_context_data(self, **kwargs):
        # Получаем базовый контекст
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст предзагруженные области с проектами
        # Можно обойтись и без использования prefetch_related - код внутри html не изменится
        # Используем prefetch_related для оптимизации и сокращения запросов к БД.
        # То есть в общем цикле мы просто используем вместо objects_list - areas_project
        context['areas_project'] = Area.objects.prefetch_related('projects')
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context['project_notes'] = project.notes.order_by('-created')
        context['project_tasks'] = project.tasks.order_by('-created')

        return context


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
        get_object_or_404(Project, pk=kwargs['pk'], author=request.user)
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
    # меняем сам queryset выводимый в object_list
    # оба способа рабочие - но в этом случае просто добавим контекст, сохранив основной queryset
    # def get_queryset(self):
    #     return Resource.objects.prefetch_related('area', 'project')


    def get_context_data(self, **kwargs):
        # Получаем базовый контекст
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст предзагруженные области с проектами
        # Можно обойтись и без использования prefetch_related - код внутри html не изменится
        # Используем prefetch_related для оптимизации и сокращения запросов к БД.
        # То есть в общем цикле мы просто используем вместо objects_list - areas_project
        context['resources_project_areas'] = Resource.objects.prefetch_related('area', 'project')
        return context



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
        get_object_or_404(Resource, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)

# DASHBOARD
# DASHBOARD
# DASHBOARD
# DASHBOARD
# DASHBOARD
# DASHBOARD
# DASHBOARD
# DASHBOARD

class DashBoardView(TemplateView):
    template_name = 'para/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем последние 5 элементов каждой модели
        context['latest_projects'] = Project.objects.order_by('-created')[:5]
        context['latest_areas'] = Area.objects.order_by('-created')[:5]
        context['latest_resources'] = Resource.objects.order_by('-created')[:5]
        context['latest_tasks'] = Task.objects.order_by('-created')[:5]
        context['latest_notes'] = Note.objects.order_by('-created')[:5]

        return context

