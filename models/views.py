from typing import Any, Dict
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse, Http404
from django.views import generic
from django.db.models import Q
from django.template import loader
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from .forms import NewUserForm, SubmitModelForm, ContactForm
from .models import (
    Psychmodel,
    Author,
    Framework,
    Language,
    Modelvariable,
    Softwarepackage,
)

from .managers import PsychmodelManager
from .filters import PsychmodelSearch, PsychmodelFilter, FrameworkSearch
from .forms import PsychmodelForm


class IndexView(generic.ListView):
    queryset = Psychmodel.objects.filter(reviewed=True)
    template_name = "models/model_overview.html"
    context_object_name = "models_list"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        # Filter by search
        self.searchset = PsychmodelSearch(self.request.GET, queryset=queryset)
        queryset = self.searchset.qs

        # Filter by filters
        self.filterset = PsychmodelFilter(self.request.GET, queryset=queryset)
        queryset = self.filterset.qs

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.searchset.form
        context["filter_form"] = self.filterset.form
        return context


class ModelView(generic.DetailView):
    model = Psychmodel
    template_name = "models/model_view.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)


def edit_model(request, pk):
    template = loader.get_template("models/model_edit.html")
    model = get_object_or_404(Psychmodel, pk=pk)
    form = PsychmodelForm(instance=model)
    if request.method == "POST":
        form = PsychmodelForm(request.POST, instance=model)
        if form.is_valid():
            model = form.save()
            messages.success(request, "Model successfuly changed.")
        else:
            messages.error(request, "Unsuccessful submission. Invalid information.")
    context = {"form": form}
    return HttpResponse(template.render(context, request))


class Frameworks(generic.ListView):
    queryset = Framework.objects.all()
    template_name = "models/frameworks_overview.html"
    context_object_name = "frameworks_list"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        self.filterset = FrameworkSearch(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.filterset.form
        return context


class FrameworkView(generic.DetailView):
    model = Framework
    template_name = "models/framework_view.html"

    def get_children(self):
        return Framework.objects.filter(parent_framework=self.object)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["children"] = self.get_children()
        return context


class SoftwareView(generic.DetailView):
    model = Softwarepackage
    template_name = "models/software.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


# Create your views here.
def index(request):
    template = loader.get_template("models/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def about(request):
    template = loader.get_template("models/about.html")
    context = {}
    return HttpResponse(template.render(context, request))


def tutorial(request):
    template = loader.get_template("models/tutorial.html")
    context = {}
    return HttpResponse(template.render(context, request))


def submit(request):
    context = {
        "login_form": AuthenticationForm(),
        # "register_form": NewUserForm(),
        "model_form": SubmitModelForm(),
    }
    if request.method == "POST":
        form = SubmitModelForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save()
            messages.success(request, "Model submission successful.")
            return redirect("models_index")
        messages.error(request, "Unsuccessful submission. Invalid information.")

    return render(request, "models/submit.html", context)


def contact(request):
    template = loader.get_template("models/contact.html")
    context = {"form": ContactForm()}

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email(recipients=["leonhard.volz@gmail.com"])
            messages.success(request, "Message sent successfully.")
            return redirect("index")
        messages.error(request, "Unsuccessful submission. Invalid information.")
    return HttpResponse(template.render(context, request))


def register_request(request):
    template = loader.get_template("registration/register.html")
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("models_index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    context = {"form": form}
    return HttpResponse(template.render(context, request))


def login_request(request):
    template = loader.get_template("registration/login.html")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    context = {"form": form}
    return HttpResponse(template.render(context, request))


def download(request):
    # check if file exists, then send it
    if "data.json" in os.listdir(MEDIA_ROOT):
        return serve(request, "data.json", MEDIA_ROOT)
    return HttpResponse("File not found.")
