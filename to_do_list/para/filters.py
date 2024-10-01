import django_filters
from django.db.models import Q

from para.models import Area


class ParaFilter(django_filters.FilterSet):
    # title = django_filters.CharFilter(lookup_expr='icontains', label='Название')
    search = django_filters.CharFilter(method='filter_by_all', label='Поиск')

    class Meta:
        model = None
        # fields = ['title', 'description']
        fields = ['search']

    def filter_by_all(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )
