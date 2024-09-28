from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse

from para.models import Project
from .models import Task
from .forms import TaskForm
from comments.forms import CommentForm


class TaskListView(ListView):
    template_name = 'tasks/task_list.html'
    model = Task
    ordering = '-id'
    paginate_by = 5
    # context_object_name = 'tasks' # обращение через tasks, а не через object_list

    def get_queryset(self):
        # Проверяем, есть ли project_id в URL
        project_id = self.request.GET.get('project_id')  # Используем GET-параметр
        resource_id = self.request.GET.get('resource_id')  # Используем GET-параметр
        area_id = self.request.GET.get('area_id')  # Используем GET-параметр
        if project_id:
            return Task.objects.filter(project_id=project_id)
        elif resource_id:
            return Task.objects.filter(resource_id=resource_id)
        elif area_id:
            return Task.objects.filter(area_id=area_id)
        else:
            return Task.objects.all()


class TaskCreateView(CreateView, LoginRequiredMixin):
    template_name = 'tasks/task_create.html'
    model = Task
    success_url = reverse_lazy('tasks:task_list')
    form_class = TaskForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class TaskUpdateView(UpdateView, LoginRequiredMixin):
    template_name = 'tasks/task_create.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект по первичному ключу и автору или вызываем 404 ошибку.
        get_object_or_404(Task, pk=kwargs['pk'], author=request.user)
        # Если объект был найден, то вызываем родительский метод,
        # чтобы работа CBV продолжилась.
        return super().dispatch(request, *args, **kwargs)


class TaskDeleteView(DeleteView, LoginRequiredMixin):
    template_name = 'tasks/task_confirm_delete.html'
    model = Task
    success_url = reverse_lazy('tasks:task_list')

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Task, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class TaskDetailView(DetailView, LoginRequiredMixin):
    template_name = 'tasks/task_detail.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['comments'] = task.comments.filter(active=True)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()  # Получаем задачу напрямую
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # Устанавливаем автора
            comment.task = task  # Устанавливаем задачу
            comment.save()
            return redirect('tasks:task_detail', pk=task.pk)
        return self.render_to_response(self.get_context_data(form=form))
