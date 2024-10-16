import django_filters
from django.db.models import Q


class ParaFilter(django_filters.FilterSet):
    """
    Custom filter set for filtering models in the PARA project.
    This filter set provides a search functionality that looks for a
    substring in both the title and description fields of the model.
    """

    search = django_filters.CharFilter(method='filter_by_all', label='Поиск')

    class Meta:
        model = None  # Should be set in subclasses to specify the model to filter.
        fields = ['search']

    def filter_by_all(self, queryset, name, value):
        """
        Custom filter method to search by title and description.
        """
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )
