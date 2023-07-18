from typing import Any, Dict
from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse, Http404
from django.views import generic
from django.db.models import Q
from django.template import loader
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from .forms import NewUserForm, SubmitModelForm, ContactForm, SearchForm
from .models import Psychmodel, Author, Framework, Language, Modelvariable
from .managers import PsychmodelManager


class IndexView(generic.ListView):
    template_name = "models/overview.html"
    form_class = SearchForm
    context_object_name = "models_list"

    def get_queryset(self, *args, **kwargs):
        psych_models = Psychmodel.objects.filter(reviewed=True)
        search_form = self.form_class(self.request.GET or None)
        if self.request.method == "GET":
            query = Q()

            if search_form.is_valid():
                name = search_form.cleaned_data.get("name")
                author = search_form.cleaned_data.get("author")
                framework = search_form.cleaned_data.get("framework")
                language = search_form.cleaned_data.get("language")
                variables = search_form.cleaned_data.get("variables")

                if name:
                    query &= Q(model_name__icontains=name)
                if author:
                    author_query = Author.objects.filter(
                        first_name__icontains=author
                    ) | Author.objects.filter(last_name__icontains=author)
                    query &= Q(publication__authors__in=author_query)
                if framework:
                    framework_query = Framework.objects.filter(
                        framework_name__icontains=framework
                    )
                    query &= Q(framework__in=framework_query)
                if language:
                    language_query = Language.objects.filter(
                        language_name__icontains=language
                    )
                    query &= Q(language__in=language_query)
                if variables:
                    variables_query = Modelvariable.objects.filter(
                        name__icontains=variables
                    )
                    query &= Q(modelvariables__in=variables_query)

                if query:
                    psych_models = psych_models.filter(query)

        return psych_models

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET)
        return context


class ModelView(generic.DetailView):
    model = Psychmodel
    template_name = "models/model_view.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)


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


def overview(request):
    template = loader.get_template("models/overview.html")
    context = {}
    return HttpResponse(template.render(context, request))


# def model_view(request, model_id):
#     model = get_object_or_404(Psychmodel, pk=model_id)
#     try:
#         framework = model.framework_set.get(pk=request.POST["framework"])
#     except (KeyError, Framework.DoesNotExist):
#         return render(request, "models/model_view.html", {"model": model, "error_message": "You did not select a valid framework."})
#     template = loader.get_template("models/model_view.html")
#     context = {"model": model}
#     return HttpResponse(template.render(context, request))


def submit(request):
    context = {
        "login_form": AuthenticationForm(),
        # "register_form": NewUserForm(),
        "model_form": SubmitModelForm(),
    }
    return render(request, "models/submit.html", context)


def submit_anon(request):
    if request.method == "POST":
        form = SubmitModelForm(request.POST, request.FILES)
        if form.is_valid():
            # model = form.save()
            messages.success(request, "Model submission successful.")
            return redirect("models_index")
        messages.error(request, "Unsuccessful submission. Invalid information.")
    form = SubmitModelForm()
    context = {"model_form": form}
    return render(request, "registration/submit_anon.html", context)


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
