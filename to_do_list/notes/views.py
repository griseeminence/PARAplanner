from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note


class NoteListView(ListView):
    template_name = 'note/note_list.html'
    model = Note
    ordering = '-id'
    paginate_by = 4

    def get_queryset(self):
        # Проверяем, есть ли project_id в URL
        project_id = self.request.GET.get('project_id')  # Используем GET-параметр
        if project_id:
            return Note.objects.filter(project_id=project_id)
        return Note.objects.all()


class NoteDetailView(DetailView):
    template_name = 'note/note_detail.html'
    model = Note


class NoteCreateView(CreateView):
    template_name = 'note/note_create.html'
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy('notes:note_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteUpdateView(UpdateView):
    template_name = 'note/note_create.html'
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy('notes:note_list')


class NoteDeleteView(DeleteView):
    template_name = 'note/note_confirm_delete.html'
    model = Note
    success_url = reverse_lazy('notes:note_list')

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Note, pk=kwargs['pk'], author=request.user)
        return super().dispatch(request, *args, **kwargs)
