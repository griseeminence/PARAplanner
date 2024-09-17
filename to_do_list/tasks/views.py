from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Task
from .forms import TaskForm


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


class TaskUpdateView(UpdateView, LoginRequiredMixin):
    template_name = 'tasks/create.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:list')


class TaskDeleteView(DeleteView, LoginRequiredMixin):
    template_name = 'tasks/task_confirm_delete.html'
    model = Task
    success_url = reverse_lazy('tasks:list')


class TaskDetailView(DetailView, LoginRequiredMixin):
    template_name = 'tasks/task_detail.html'
    model = Task
