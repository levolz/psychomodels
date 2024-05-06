import django_filters
from django.db.models import Q

from django import forms

from .models import Phenomenon, Fact


class PhenomenonSearch(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="filter_search",
        label="Search",
    )

    class Meta:
        model = Phenomenon
        fields = [
            "search",
        ]

    def filter_search(self, queryset, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        )


class PhenomenonFilter(django_filters.FilterSet):
    class Meta:
        model = Phenomenon
        fields = ["field", "constructs"]
