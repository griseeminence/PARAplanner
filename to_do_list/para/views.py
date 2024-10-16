from django_filters.views import FilterView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, TemplateView

from comments.forms import CommentForm
from comments.utils import handle_comment_creation, handle_comment_deletion, handle_comment_editing, handle_edit_request
from core.models import ParaTag
from notes.models import Note
from para.filters import ParaFilter
from para.forms import AreaForm, ProjectForm, ResourceForm
from para.models import Area, Project, Resource
from tasks.models import Task


class AreaListView(FilterView):
    """
    A view for displaying a filtered and paginated list of areas.

    Methods:
        get_queryset(): Returns the queryset of areas, filtered by project, resource, or area if applicable.
        get_context_data(**kwargs): Extends the context with additional information if needed.
    """

    template_name = 'para/area_list.html'
    model = Area
    ordering = '-id'
    paginate_by = 3
    filterset_class = ParaFilter

    def get_queryset(self):
        """
        Returns a queryset of Area instances, applying filters.
        """

        # Optimizing queries with prefetch_related
        queryset = Area.objects.prefetch_related('projects').order_by(self.ordering)
        # Dynamically assign the model for filtering.
        self.filterset_class.Meta.model = Area
        return self.filterset_class(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs):
        """
        Adds additional context to the view.
        Can be extended if more data needs to be passed to the template.
        """

        context = super().get_context_data(**kwargs)
        return context


class AreaDetailView(DetailView):
    """
    A view for displaying detailed information about a specific Area, including its comments.
    Requires user authentication.

    Methods:
        get_context_data(**kwargs): Adds comments and a comment form to the context.
        post(request, *args, **kwargs): Handles various comment-related actions (creation, editing, deletion).
    """

    template_name = 'para/area_detail.html'
    redirect_url = 'para:area_detail'
    model = Area

    def get_context_data(self, **kwargs):
        """
        Adds additional context to the template, including notes, tasks, and comments.
        """

        context = super().get_context_data(**kwargs)
        area = self.object
        context['area_notes'] = area.notes.order_by('-created')
        context['area_tasks'] = area.tasks.order_by('-created')
        context['comments'] = area.comments.filter(active=True).order_by('-created')
        context['comment_form'] = CommentForm()
        context['editing_comment'] = None
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request to manage comments for the Area.

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


class AreaCreateView(CreateView):
    """
    A view for creating a new area. Requires user authentication.

    Methods:
        form_valid(form): Processes valid form data, assigns the author, saves the image if provided,
        and adds a new tag to the area if specified.
    """

    template_name = 'para/area_create.html'
    model = Area
    success_url = reverse_lazy('para:area_list')
    form_class = AreaForm

    def form_valid(self, form):
        """
        Handles the saving of the area form. Assigns the current user as the areas author,
        saves the cover image if uploaded, and adds a new tag if entered by the user.
        """

        area = form.save(commit=False)
        area.author = self.request.user
        if 'cover_image' in self.request.FILES:
            area.cover_image = self.request.FILES['cover_image']
        area.save()
        form.save_m2m()
        new_tag = form.cleaned_data.get('new_tag')
        if new_tag:
            tag, created = ParaTag.objects.get_or_create(title=new_tag)
            area.tags.add(tag)
        return super().form_valid(form)


class AreaUpdateView(UpdateView):
    """
    A view for updating an existing area. Requires user authentication.
    """

    template_name = 'para/area_create.html'
    model = Area
    form_class = AreaForm
    success_url = reverse_lazy('para:area_list')


class AreaDeleteView(DeleteView):
    """
    A view for deleting an existing area. Requires user authentication.

    Methods:
        dispatch(request, *args, **kwargs): Ensures that only the areas author can access the delete view.
    """

    template_name = 'para/area_confirm_delete.html'
    model = Area
    success_url = reverse_lazy('para:area_list')

    def dispatch(self, request, *args, **kwargs):
        """
        Ensures the user is the author of the area before proceeding with the request.
        """

        get_object_or_404(Area, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


# PROJECTS

class ProjectListView(FilterView):
    """
    A view for displaying a filtered and paginated list of projects.

    Methods:
        get_queryset(): Returns the queryset of projects, filtered by project, resource, or area if applicable.
        get_context_data(**kwargs): Extends the context with additional information if needed.
    """

    template_name = 'para/project_list.html'
    model = Project
    ordering = '-id'
    paginate_by = 3
    filterset_class = ParaFilter

    def get_queryset(self):
        """
        Returns a queryset of Project instances, applying filters.
        """

        queryset = Project.objects.all()
        # Dynamically assign the model for filtering.
        self.filterset_class.Meta.model = Project
        return self.filterset_class(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProjectDetailView(DetailView):
    """
    A view for displaying detailed information about a specific Project, including its comments.
    Requires user authentication.

    Methods:
        get_context_data(**kwargs): Adds comments and a comment form to the context.
        post(request, *args, **kwargs): Handles various comment-related actions (creation, editing, deletion).
    """
    template_name = 'para/project_detail.html'
    redirect_url = 'para:project_detail'
    model = Project

    def get_context_data(self, **kwargs):
        """
        Adds additional context to the template, including notes, tasks, and comments.
        """

        context = super().get_context_data(**kwargs)
        project = self.object
        context['project_notes'] = project.notes.order_by('-created')
        context['project_tasks'] = project.tasks.order_by('-created')
        context['comments'] = project.comments.filter(active=True).order_by('-created')
        context['comment_form'] = CommentForm()
        context['editing_comment'] = None
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request to manage comments for the Area.

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


class ProjectCreateView(CreateView):
    """
    A view for creating a new project. Requires user authentication.

    Methods:
        form_valid(form): Processes valid form data, assigns the author, saves the image if provided,
        and adds a new tag to the project if specified.
    """

    template_name = 'para/project_create.html'
    model = Project
    success_url = reverse_lazy('para:project_list')
    form_class = ProjectForm

    def form_valid(self, form):
        """
        Handles the saving of the project form. Assigns the current user as the project's author,
        saves the cover image if uploaded, and adds a new tag if entered by the user.
        """

        project = form.save(commit=False)
        project.author = self.request.user
        if 'cover_image' in self.request.FILES:
            project.cover_image = self.request.FILES['cover_image']
        project.save()
        form.save_m2m()
        new_tag = form.cleaned_data.get('new_tag')
        if new_tag:
            tag, created = ParaTag.objects.get_or_create(title=new_tag)
            project.tags.add(tag)
        return super().form_valid(form)


class ProjectUpdateView(UpdateView):
    """
    A view for updating an existing project. Requires user authentication.
    """

    template_name = 'para/project_create.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('para:project_list')


class ProjectDeleteView(DeleteView):
    """
    A view for deleting an existing project. Requires user authentication.

    Methods:
        dispatch(request, *args, **kwargs): Ensures that only the project's author can access the delete view.
    """

    template_name = 'para/project_confirm_delete.html'
    model = Project
    success_url = reverse_lazy('para:project_list')

    def dispatch(self, request, *args, **kwargs):
        """
        Ensures the user is the author of the project before proceeding with the request.
        """

        get_object_or_404(Project, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


# RESOURCES

class ResourceListView(FilterView):
    """
    A view for displaying a filtered and paginated list of resources.

    Methods:
        get_queryset(): Returns the queryset of resources, filtered by project, resource, or area if applicable.
        get_context_data(**kwargs): Extends the context with additional information if needed.
    """

    template_name = 'para/resource_list.html'
    model = Resource
    ordering = '-id'
    paginate_by = 3
    filterset_class = ParaFilter

    def get_queryset(self):
        """
        Returns a queryset of Area instances, applying filters.
        """

        # Optimizing queries with prefetch_related
        queryset = Resource.objects.prefetch_related('area', 'project').order_by(self.ordering)
        # Dynamically assign the model for filtering.
        self.filterset_class.Meta.model = Project
        return self.filterset_class(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs):
        """
        Adds additional context to the view.
        Can be extended if more data needs to be passed to the template.
        """

        context = super().get_context_data(**kwargs)
        return context


class ResourceDetailView(DetailView):
    """
    A view for displaying detailed information about a specific Resource, including its comments.
    Requires user authentication.

    Methods:
        get_context_data(**kwargs): Adds comments and a comment form to the context.
        post(request, *args, **kwargs): Handles various comment-related actions (creation, editing, deletion).
    """

    template_name = 'para/resource_detail.html'
    redirect_url = 'para:resource_detail'
    model = Resource

    def get_context_data(self, **kwargs):
        """
        Adds additional context to the template, including notes, tasks, and comments.
        """

        context = super().get_context_data(**kwargs)
        resource = self.object
        context['resource_notes'] = resource.notes.order_by('-created')
        context['resource_tasks'] = resource.tasks.order_by('-created')
        context['comments'] = resource.comments.filter(active=True).order_by('-created')
        context['comment_form'] = CommentForm()
        context['editing_comment'] = None
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request to manage comments for the Area.

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


class ResourceCreateView(CreateView):
    """
    A view for creating a new resource. Requires user authentication.

    Methods:
        form_valid(form): Processes valid form data, assigns the author, saves the image if provided,
        and adds a new tag to the resource if specified.
    """

    template_name = 'para/resource_create.html'
    model = Resource
    success_url = reverse_lazy('para:resource_list')
    form_class = ResourceForm

    def form_valid(self, form):
        """
        Handles the saving of the resource form. Assigns the current user as the resources author,
        saves the cover image if uploaded, and adds a new tag if entered by the user.
        """

        resource = form.save(commit=False)
        resource.author = self.request.user
        if 'cover_image' in self.request.FILES:
            resource.cover_image = self.request.FILES['cover_image']
        resource.save()
        form.save_m2m()
        new_tag = form.cleaned_data.get('new_tag')
        if new_tag:
            tag, created = ParaTag.objects.get_or_create(title=new_tag)
            resource.tags.add(tag)
        return super().form_valid(form)


class ResourceUpdateView(UpdateView):
    """
    A view for updating an existing resource. Requires user authentication.
    """

    template_name = 'para/resource_create.html'
    model = Resource
    form_class = ResourceForm
    success_url = reverse_lazy('para:resource_list')


class ResourceDeleteView(DeleteView):
    """
    A view for deleting an existing resource. Requires user authentication.

    Methods:
        dispatch(request, *args, **kwargs): Ensures that only the resources author can access the delete view.
    """

    template_name = 'para/resource_confirm_delete.html'
    model = Resource
    success_url = reverse_lazy('para:resource_list')

    def dispatch(self, request, *args, **kwargs):
        """
        Ensures the user is the author of the resource before proceeding with the request.
        """

        get_object_or_404(Resource, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)


# DASHBOARD

class DashBoardView(TemplateView):
    """
    View for displaying the dashboard with the latest entries from various models.
    """

    template_name = 'para/dashboard.html'

    def get_context_data(self, **kwargs):
        """
        Adds the latest entries from different models to the context.

        Returns:
            dict: Updated context data with the latest projects, areas, resources, tasks, and notes.
        """
        context = super().get_context_data(**kwargs)

        # Retrieve the latest 5 entries for each model
        context['latest_projects'] = Project.objects.order_by('-created')[:5]
        context['latest_areas'] = Area.objects.order_by('-created')[:5]
        context['latest_resources'] = Resource.objects.order_by('-created')[:5]
        context['latest_tasks'] = Task.objects.order_by('-created')[:5]
        context['latest_notes'] = Note.objects.order_by('-created')[:5]

        return context
