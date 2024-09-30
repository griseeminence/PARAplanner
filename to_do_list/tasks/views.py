from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse

from para.models import Project
from .models import Task
from .forms import TaskForm
from comments.forms import CommentForm
from comments.utils import get_comment, user_is_author, handle_comment_creation, handle_comment_deletion, \
    handle_comment_editing, handle_edit_request

class TaskListView(ListView):
    template_name = 'tasks/task_list.html'
    model = Task
    ordering = '-id'
    paginate_by = 3
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
    redirect_url = 'tasks:task_detail'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['comments'] = task.comments.filter(active=True).order_by('-created')
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
