from urllib import request

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse

from comments.forms import CommentForm
from comments.models import Comment
from notes.models import Note
from para.forms import AreaForm, ProjectForm, ResourceForm
from para.models import Area, Project, Resource, ResourceType
from tasks.models import Task
from comments.utils import get_comment, user_is_author, handle_comment_creation, handle_comment_deletion, \
    handle_comment_editing, handle_edit_request


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
    paginate_by = 3

    def get_queryset(self):
        # Оптимизация запросов с prefetch_related
        return Area.objects.prefetch_related('projects').order_by(self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AreaDetailView(DetailView):
    template_name = 'para/area_detail.html'
    redirect_url = 'para:area_detail'
    model = Area

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        area = self.object
        context['area_notes'] = area.notes.order_by('-created')
        context['area_tasks'] = area.tasks.order_by('-created')
        context['comments'] = area.comments.filter(active=True).order_by('-created')
        context['comment_form'] = CommentForm()
        context['editing_comment'] = None
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Получаем объект проекта

        # Обработка добавления нового комментария
        if 'submit_comment' in request.POST:
            return handle_comment_creation(request, self.object, self.redirect_url)

        # Обработка редактирования комментария
        elif 'edit_comment' in request.POST:
            return handle_comment_editing(request, self.object, self.redirect_url)

        # Обработка запроса на редактирование комментария
        elif 'edit' in request.POST:
            context = handle_edit_request(request, self.object, self.get_context_data)
            if context:
                return self.render_to_response(context)

        # Обработка удаления комментария
        elif 'delete_comment' in request.POST:
            return handle_comment_deletion(request, self.object, self.redirect_url)

        return self.get(request, *args, **kwargs)


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
    paginate_by = 3


class ProjectDetailView(DetailView):
    template_name = 'para/project_detail.html'
    redirect_url = 'para:project_detail'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context['project_notes'] = project.notes.order_by('-created')
        context['project_tasks'] = project.tasks.order_by('-created')
        context['comments'] = project.comments.filter(active=True).order_by('-created')
        context['comment_form'] = CommentForm()
        context['editing_comment'] = None
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Получаем объект проекта

        # Обработка добавления нового комментария
        if 'submit_comment' in request.POST:
            return handle_comment_creation(request, self.object, self.redirect_url)

        # Обработка редактирования комментария
        elif 'edit_comment' in request.POST:
            return handle_comment_editing(request, self.object, self.redirect_url)

        # Обработка запроса на редактирование комментария
        elif 'edit' in request.POST:
            context = handle_edit_request(request, self.object, self.get_context_data)
            if context:
                return self.render_to_response(context)

        # Обработка удаления комментария
        elif 'delete_comment' in request.POST:
            return handle_comment_deletion(request, self.object, self.redirect_url)

        return self.get(request, *args, **kwargs)


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
    paginate_by = 3

    # меняем сам queryset выводимый в object_list
    # оба способа рабочие - но в этом случае просто добавим контекст, сохранив основной queryset
    # def get_queryset(self):
    #     return Resource.objects.prefetch_related('area', 'project')

    def get_queryset(self):
        # Оптимизация запросов с prefetch_related
        return Resource.objects.prefetch_related('area', 'project')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ResourceDetailView(DetailView):
    template_name = 'para/resource_detail.html'
    redirect_url = 'para:resource_detail'
    model = Resource

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = self.object
        context['resource_notes'] = resource.notes.order_by('-created')
        context['resource_tasks'] = resource.tasks.order_by('-created')
        context['comments'] = resource.comments.filter(active=True).order_by('-created')
        context['comment_form'] = CommentForm()
        context['editing_comment'] = None
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Получаем объект проекта

        # Обработка добавления нового комментария
        if 'submit_comment' in request.POST:
            return handle_comment_creation(request, self.object, self.redirect_url)

        # Обработка редактирования комментария
        elif 'edit_comment' in request.POST:
            return handle_comment_editing(request, self.object, self.redirect_url)

        # Обработка запроса на редактирование комментария
        elif 'edit' in request.POST:
            context = handle_edit_request(request, self.object, self.get_context_data)
            if context:
                return self.render_to_response(context)

        # Обработка удаления комментария
        elif 'delete_comment' in request.POST:
            return handle_comment_deletion(request, self.object, self.redirect_url)

        return self.get(request, *args, **kwargs)


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
