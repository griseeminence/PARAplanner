from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect

from comments.forms import CommentForm
from comments.models import Comment


def get_comment(comment_id, obj, model):
    """Получение комментария по id для указанной модели"""
    try:
        return Comment.objects.get(
            id=comment_id,
            content_type=ContentType.objects.get_for_model(model),
            object_id=obj.id
        )
    except Comment.DoesNotExist:
        return None


def user_is_author(comment, user):
    """Проверка, является ли пользователь автором комментария"""
    return user == comment.author


def handle_comment_creation(request, obj, redirect_url):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.author = request.user
        comment.content_object = obj
        comment.save()
        return redirect(redirect_url, pk=obj.pk)


def handle_comment_editing(request, obj, redirect_url):
    comment_id = request.POST.get('comment_id')
    comment_text = request.POST.get('text')
    comment = get_comment(comment_id, obj, type(obj))

    if comment and user_is_author(comment, request.user):
        comment.text = comment_text
        comment.save()
        return redirect(redirect_url, pk=obj.pk)


def handle_edit_request(request, obj, get_context_data_func):
    comment_id = request.POST.get('comment_id')
    comment = get_comment(comment_id, obj, type(obj))

    if comment and user_is_author(comment, request.user):
        context = get_context_data_func()
        context['editing_comment'] = comment
        context['comment_form'] = CommentForm(initial={'text': comment.text})
        return context


def handle_comment_deletion(request, obj, redirect_url):
    comment_id = request.POST.get('comment_id')
    comment = get_comment(comment_id, obj, type(obj))

    if comment and user_is_author(comment, request.user):
        comment.delete()
        return redirect(redirect_url, pk=obj.pk)
