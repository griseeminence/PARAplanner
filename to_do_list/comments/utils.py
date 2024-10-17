from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, get_object_or_404

from comments.forms import CommentForm
from comments.models import Comment


def get_comment(comment_id, obj, model):
    """
    Retrieve a specific comment by its ID and the associated object.
    Uses get_object_or_404 to avoid manual exception handling.
    """
    content_type = ContentType.objects.get_for_model(type(obj))
    return get_object_or_404(Comment, id=comment_id, content_type=content_type, object_id=obj.id)


def user_is_author(comment, user):
    """
    Check if the user is the author of the given comment.
    """
    return comment.author_id == user.id  # Optimized comparison


def handle_comment_creation(request, obj, redirect_url):
    """
    Handle the creation of a new comment and link it to an object.
    """
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.content_object = obj
        comment.save()
        return redirect(redirect_url, pk=obj.pk)
    return None  # Optional: Handle invalid form cases if needed


def handle_comment_editing(request, obj, redirect_url):
    """
    Handle the editing of an existing comment.
    """
    comment_id = request.POST.get('comment_id')
    comment = get_comment(comment_id, obj, type(obj))

    if user_is_author(comment, request.user):
        comment.text = request.POST.get('text', comment.text)  # Update only if text provided
        comment.save()
        return redirect(redirect_url, pk=obj.pk)
    return None  # Optional: Handle unauthorized access


def handle_edit_request(request, obj, get_context_data_func):
    """
    Prepare context data for rendering a comment-editing form.
    """
    comment_id = request.POST.get('comment_id')
    comment = get_comment(comment_id, obj, type(obj))

    if user_is_author(comment, request.user):
        context = get_context_data_func()
        context.update({
            'editing_comment': comment,
            'comment_form': CommentForm(initial={'text': comment.text})
        })
        return context
    return {}  # Optional: Handle unauthorized access


def handle_comment_deletion(request, obj, redirect_url):
    """
    Handle the deletion of an existing comment.
    """
    comment_id = request.POST.get('comment_id')
    comment = get_comment(comment_id, obj, type(obj))

    if user_is_author(comment, request.user):
        comment.delete()
        return redirect(redirect_url, pk=obj.pk)
    return None  # Optional: Handle unauthorized access
