from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Task
from .forms import TaskForm

class TasksListView(ListView):
    template_name = 'tasks/list.html'
    model = Task
    ordering = 'id'
    paginate_by = 10
    # form_class = TaskForm
    # context_object_name = 'tasks' # обращение через tasks, а не через object_list