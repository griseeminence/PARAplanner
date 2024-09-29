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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        area = self.object
        context['area_notes'] = area.notes.order_by('-created')
        context['area_tasks'] = area.tasks.order_by('-created')

        return context


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
        context['comments'] = project.comments.filter(active=True).order_by('-created')
        context['comment_form'] = CommentForm()
        context['editing_comment'] = None
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Получаем объект проекта

        # Обработка добавления нового комментария
        if 'submit_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.content_object = self.object  # используем self.object
                comment.save()
                return redirect('para:project_detail', pk=self.object.pk)  # обновляем страницу с комментариями

        # Обработка редактирования комментария
        elif 'edit_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment_text = request.POST.get('text')  # Извлекаем текст комментария из формы
            try:
                comment = Comment.objects.get(
                    id=comment_id,
                    content_type=ContentType.objects.get_for_model(Project),
                    object_id=self.object.id
                )
                if request.user == comment.author:
                    comment.text = comment_text  # Обновляем текст комментария
                    comment.save()  # Сохраняем изменения
                    return redirect('para:project_detail', pk=self.object.pk)
            except Comment.DoesNotExist:
                return self.get(request, *args, **kwargs)

        # Обработка запроса на редактирование комментария
        elif 'edit' in request.POST:
            comment_id = request.POST.get('comment_id')
            try:
                editing_comment = Comment.objects.get(
                    id=comment_id,
                    content_type=ContentType.objects.get_for_model(Project),
                    object_id=self.object.id  # используем self.object
                )
                if request.user == editing_comment.author:
                    # Создаем экземпляр формы для редактирования комментария
                    # edit_comment_form = CommentForm(instance=editing_comment)
                    # Передаем комментарий и форму для редактирования в контекст
                    context = self.get_context_data(**kwargs)
                    context['editing_comment'] = editing_comment
                    context['comment_form'] = CommentForm(initial={'text': editing_comment.text})
                    return self.render_to_response(context)
            except Comment.DoesNotExist:
                return self.get(request, *args, **kwargs)

        # Обработка удаления комментария
        elif 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            try:
                comment = Comment.objects.get(
                    id=comment_id,
                    content_type=ContentType.objects.get_for_model(Project),
                    object_id=self.object.id  # используем self.object
                )
                if request.user == comment.author:
                    comment.delete()
                    return HttpResponseRedirect(reverse('para:project_detail', kwargs={'pk': self.object.pk}))
            except Comment.DoesNotExist:
                return self.get(request, *args, **kwargs)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource = self.object
        context['resource_notes'] = resource.notes.order_by('-created')
        context['resource_tasks'] = resource.tasks.order_by('-created')

        return context


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
