import django_filters
from django.db.models import Q

from notes.models import Note
from para.models import Area


class NoteFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_all', label='Поиск')

    class Meta:
        model = Note
        fields = ['search']

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(content__icontains=value)
        )
