from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse

from django.views import generic

from .models import Phenomenon, Construct, Fact
from .filters import PhenomenonSearch, PhenomenonFilter


def index(request):
    template = loader.get_template("facts/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


class PhenomenaView(generic.ListView):
    model = Phenomenon
    template_name = "facts/phenomena.html"
    context_object_name = "phenomena_list"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        self.searchset = PhenomenonSearch(self.request.GET, queryset=queryset)
        queryset = self.searchset.qs

        self.filterset = PhenomenonFilter(self.request.GET, queryset=queryset)
        queryset = self.filterset.qs

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.searchset.form
        context["filter_form"] = self.filterset.form
        return context


class PhenomenonView(generic.DetailView):
    model = Phenomenon
    template_name = "facts/phenomenon_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ConstructsView(generic.ListView):
    model = Construct
    template_name = "facts/constructs.html"
    context_object_name = "construct_list"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class ConstructView(generic.DetailView):
    model = Construct
    template_name = "facts/construct_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FactsView(generic.ListView):
    model = Fact
    template_name = "facts/facts.html"
    context_object_name = "facts_list"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class FactView(generic.DetailView):
    model = Fact
    template_name = "facts/fact_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
