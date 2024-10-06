from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse
from django_filters.views import FilterView

from comments.forms import CommentForm
from core.models import ParaTag
from notes.filters import NoteFilter
from notes.forms import NoteForm
from notes.models import Note
from comments.utils import get_comment, user_is_author, handle_comment_creation, handle_comment_deletion, \
    handle_comment_editing, handle_edit_request


class NoteListView(FilterView):
    template_name = 'note/note_list.html'
    model = Note
    ordering = '-id'
    paginate_by = 6
    filterset_class = NoteFilter

    def get_queryset(self):
        # Проверяем, есть ли project_id в URL
        project_id = self.request.GET.get('project_id')  # Используем GET-параметр
        resource_id = self.request.GET.get('resource_id')  # Используем GET-параметр
        area_id = self.request.GET.get('area_id')  # Используем GET-параметр
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
        context = super().get_context_data(**kwargs)
        return context


class NoteDetailView(DetailView):
    template_name = 'note/note_detail.html'
    redirect_url = 'notes:note_detail'
    model = Note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        note = self.object
        context['comments'] = note.comments.filter(active=True).order_by('-created')
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


class NoteCreateView(CreateView):
    template_name = 'note/note_create.html'
    model = Note
    form_class = NoteForm
    success_url = reverse_lazy('notes:note_list')

    def form_valid(self, form):
        note = form.save(commit=False)
        note.author = self.request.user
        note.save()  # Теперь мы сохраняем заметку и получаем ID

        # Теперь добавляем теги после сохранения заметки
        new_tag = form.cleaned_data.get('new_tag')
        if new_tag:
            tag, created = ParaTag.objects.get_or_create(title=new_tag)
            note.tags.add(tag)  # Теперь это безопасно

        # Сохраняем многие-ко-многим отношения
        form.save_m2m()  # Это сохранит другие многие-ко-многим отношения

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
