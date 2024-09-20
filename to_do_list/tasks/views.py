from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import Task
from .forms import TaskForm
from comments.forms import CommentForm


class TaskListView(ListView):
    template_name = 'tasks/list.html'
    model = Task
    ordering = '-id'
    paginate_by = 4
    # context_object_name = 'tasks' # обращение через tasks, а не через object_list


class TaskCreateView(CreateView, LoginRequiredMixin):
    template_name = 'tasks/create.html'
    model = Task
    success_url = reverse_lazy('tasks:list')
    form_class = TaskForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class TaskUpdateView(UpdateView, LoginRequiredMixin):
    template_name = 'tasks/create.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:list')

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект по первичному ключу и автору или вызываем 404 ошибку.
        get_object_or_404(Task, pk=kwargs['pk'], author=request.user)
        # Если объект был найден, то вызываем родительский метод,
        # чтобы работа CBV продолжилась.
        return super().dispatch(request, *args, **kwargs)


class TaskDeleteView(DeleteView, LoginRequiredMixin):
    template_name = 'tasks/task_confirm_delete.html'
    model = Task
    success_url = reverse_lazy('tasks:list')

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
        task = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            # Сохраняем комментарий, не отправляя его в базу данных (commit=False)
            comment = form.save(commit=False)
            # Привязываем комментарий к задаче и пользователю
            comment.task = task
            comment.author = request.user
            comment.save()
            # Перенаправляем пользователя на ту же страницу задачи
            return redirect(reverse('tasks:detail', kwargs={'pk': task.pk}))

        # Если форма не валидна, возвращаемся на страницу с ошибками
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)
