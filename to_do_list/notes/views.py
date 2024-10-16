from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from comments.forms import CommentForm
from core.models import ParaTag
from notes.filters import NoteFilter
from notes.forms import NoteForm
from notes.models import Note
from comments.utils import handle_comment_creation, handle_comment_deletion, handle_comment_editing, handle_edit_request


class NoteListView(FilterView):
    """
    A view for displaying a filtered and paginated list of notes.

    Methods:
        get_queryset(): Returns the queryset of areas, filtered by project, resource, or area if applicable.
        get_context_data(**kwargs): Extends the context with additional information if needed.
    """

    template_name = 'note/note_list.html'
    model = Note
    ordering = '-id'
    paginate_by = 6
    filterset_class = NoteFilter

    def get_queryset(self):
        """
        Fetches the task queryset. Filters tasks based on query parameters
        like project_id, resource_id, or area_id from the request's GET data.
        If no such parameter is found, it applies a general filter using the filter class.
        """

        project_id = self.request.GET.get('project_id')
        resource_id = self.request.GET.get('resource_id')
        area_id = self.request.GET.get('area_id')
        queryset = Note.objects.all()
        if project_id:
            return Note.objects.filter(project_id=project_id)
        elif resource_id:
            return Note.objects.filter(resource_id=resource_id)
        elif area_id:
            return Note.objects.filter(area_id=area_id)
        else:
            return self.filterset_class(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs):
        """
        Adds additional context to the view.
        Can be extended if more data needs to be passed to the template.
        """

        context = super().get_context_data(**kwargs)
        return context


class NoteDetailView(DetailView):
    """
    A view for displaying detailed information about a specific Note, including its comments.
    Requires user authentication.

    Methods:
        get_context_data(**kwargs): Adds comments and a comment form to the context.
        post(request, *args, **kwargs): Handles various comment-related actions (creation, editing, deletion).
    """

    template_name = 'note/note_detail.html'
    redirect_url = 'notes:note_detail'
    model = Note

    def get_context_data(self, **kwargs):
        """
        Adds additional context to the template, including notes, tasks, and comments.
        """

        context = super().get_context_data(**kwargs)
        note = self.object
        context['comments'] = note.comments.filter(active=True).order_by('-created')
        context['comment_form'] = CommentForm()
        context['editing_comment'] = None
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request to manage comments for the Note.

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


class NoteCreateView(CreateView):
    """
    A view for creating a new note. Requires user authentication.

    Methods:
        form_valid(form): Processes valid form data, assigns the author, saves the image if provided,
        and adds a new tag to the note if specified.
    """

    template_name = 'note/note_create.html'
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy('notes:note_list')

    def form_valid(self, form):
        """
        Handles the saving of the note form. Assigns the current user as the notes author,
        saves the cover image if uploaded, and adds a new tag if entered by the user.
        """

        note = form.save(commit=False)
        note.author = self.request.user
        if 'cover_image' in self.request.FILES:
            note.cover_image = self.request.FILES['cover_image']
        note.save()
        form.save_m2m()
        new_tag = form.cleaned_data.get('new_tag')
        if new_tag:
            tag, created = ParaTag.objects.get_or_create(title=new_tag)
            note.tags.add(tag)
        return super().form_valid(form)


class NoteUpdateView(UpdateView):
    """
    A view for updating an existing note. Requires user authentication.
    """

    template_name = 'note/note_create.html'
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy('notes:note_list')


class NoteDeleteView(DeleteView):
    """
    A view for deleting an existing note. Requires user authentication.

    Methods:
        dispatch(request, *args, **kwargs): Ensures that only the notes author can access the delete view.
    """

    template_name = 'note/note_confirm_delete.html'
    model = Note
    success_url = reverse_lazy('notes:note_list')

    def dispatch(self, request, *args, **kwargs):
        """
        Ensures the user is the author of the note before proceeding with the request.
        """

        get_object_or_404(Note, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)
