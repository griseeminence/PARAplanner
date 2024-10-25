from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from core.models import ParaTag
from comments.forms import CommentForm
from comments.utils import handle_comment_creation, handle_comment_deletion, handle_comment_editing, handle_edit_request
from para.filters import ParaFilter
from para.models import Project
from .models import Task
from .forms import TaskForm


class TaskListView(FilterView):
    """
    A view for displaying a filtered and paginated list of tasks.

    Methods:
        get_queryset(): Returns the queryset of tasks, filtered by project, resource, or area if applicable.
        get_context_data(**kwargs): Extends the context with additional information if needed.
    """

    template_name = 'tasks/task_list.html'
    model = Task
    ordering = '-id'
    paginate_by = 3
    filterset_class = ParaFilter

    # context_object_name = 'tasks' # обращение через tasks, а не через object_list

    def get_queryset(self):
        """
        Fetches the task queryset. Filters tasks based on query parameters
        like project_id, resource_id, or area_id from the request's GET data.
        If no such parameter is found, it applies a general filter using the filter class.
        """

        project_id = self.request.GET.get('project_id')
        resource_id = self.request.GET.get('resource_id')
        area_id = self.request.GET.get('area_id')
        queryset = Task.objects.all()
        # Dynamically assign the model for filtering.
        self.filterset_class.Meta.model = Project
        if project_id:
            return Task.objects.filter(project_id=project_id)
        elif resource_id:
            return Task.objects.filter(resource_id=resource_id)
        elif area_id:
            return Task.objects.filter(area_id=area_id)
        else:
            return self.filterset_class(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs):
        """
        Adds additional context to the view.
        Can be extended if more data needs to be passed to the template.
        """

        context = super().get_context_data(**kwargs)
        return context


class TaskCreateView(CreateView, LoginRequiredMixin):
    """
    A view for creating a new task. Requires user authentication.

    Methods:
        form_valid(form): Processes valid form data, assigns the author, saves the image if provided,
        and adds a new tag to the task if specified.
    """

    template_name = 'tasks/task_create.html'
    model = Task
    success_url = reverse_lazy('tasks:task_list')
    form_class = TaskForm

    def form_valid(self, form):
        """
        Handles the saving of the task form. Assigns the current user as the task's author,
        saves the cover image if uploaded, and adds a new tag if entered by the user.
        """

        task = form.save(commit=False)
        task.author = self.request.user
        if 'cover_image' in self.request.FILES:
            task.cover_image = self.request.FILES['cover_image']
        task.save()
        form.save_m2m()
        new_tag = form.cleaned_data.get('new_tag')
        if new_tag:
            tag, created = ParaTag.objects.get_or_create(title=new_tag)
            task.tags.add(tag)
        return super().form_valid(form)


class TaskUpdateView(UpdateView, LoginRequiredMixin):
    """
    A view for updating an existing task. Requires user authentication.

    Methods:
        dispatch(request, *args, **kwargs): Ensures that only the task's author can access the update view.
    """

    template_name = 'tasks/task_create.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')

    def dispatch(self, request, *args, **kwargs):
        """
        Ensures the user is the author of the task before proceeding with the request.
        """
        get_object_or_404(Task, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class TaskDeleteView(DeleteView, LoginRequiredMixin):
    """
    A view for deleting an existing task. Requires user authentication.

    Methods:
        dispatch(request, *args, **kwargs): Ensures that only the task's author can access the delete view.
    """
    template_name = 'tasks/task_confirm_delete.html'
    model = Task
    success_url = reverse_lazy('tasks:task_list')

    def dispatch(self, request, *args, **kwargs):
        """
        Ensures the user is the author of the task before proceeding with the request.
        """
        get_object_or_404(Task, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


class TaskDetailView(DetailView, LoginRequiredMixin):
    """
    A view for displaying detailed information about a specific task, including its comments.
    Requires user authentication.

    Methods:
        get_context_data(**kwargs): Adds comments and a comment form to the context.
        post(request, *args, **kwargs): Handles various comment-related actions (creation, editing, deletion).
    """

    template_name = 'tasks/task_detail.html'
    redirect_url = 'tasks:task_detail'
    model = Task

    def get_context_data(self, **kwargs):
        """
        Adds comments and a comment form to the context.
        """

        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['comments'] = task.comments.filter(active=True).order_by('-created')
        context['comment_form'] = CommentForm()
        context['editing_comment'] = None
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request to manage comments for the task.

        The method processes the following actions based on the submitted form:
        - Adding a new comment
        - Editing an existing comment
        - Deleting a comment

        Note: Separate handler methods are used for each action, defined in the `comments.utils` module,
        to unify the process for different models.
        """
        self.object = self.get_object()

        if 'submit_comment' in request.POST:
            return handle_comment_creation(request, self.object, self.redirect_url)

        elif 'edit_comment' in request.POST:
            return handle_comment_editing(request, self.object, self.redirect_url)

        elif 'edit' in request.POST:
            context = handle_edit_request(request, self.object, self.get_context_data)
            if context:
                return self.render_to_response(context)

        elif 'delete_comment' in request.POST:
            return handle_comment_deletion(request, self.object, self.redirect_url)

        return self.get(request, *args, **kwargs)
