import django_filters
from django.db.models import Q

from django import forms

from .models import Psychmodel


class PsychmodelSearch(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name="model_name",
        lookup_expr="icontains",
        label="Title",
    )

    # framework = django_filters.CharFilter(
    #     field_name="framework__framework_name",
    #     lookup_expr="icontains",
    #     label="Framework",
    # )
    # language = django_filters.CharFilter(
    #     lookup_expr="icontains",
    #     label="Programming Language",
    # )
    vars = django_filters.CharFilter(
        field_name="modelvariables__name",
        lookup_expr="icontains",
        label="Variables",
    )

    authors = django_filters.CharFilter(
        method="filter_authors",
        label="Authors",
    )

    class Meta:
        model = Psychmodel
        fields = [
            "title",
            "authors",
            # "framework", "language",
            "vars",
        ]

    def filter_authors(self, queryset, name, value):
        return queryset.filter(
            Q(publication__authors__first_name__icontains=value)
            | Q(publication__authors__last_name__icontains=value)
        )


class PsychmodelFilter(django_filters.FilterSet):
    class Meta:
        model = Psychmodel
        fields = ["framework", "language", "psychfield"]
