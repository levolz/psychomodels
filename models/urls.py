from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="models_index"),
    path("about/", views.about, name="models_about"),
    path("tutorial/", views.tutorial, name="models_tutorial"),
    path("models/", views.IndexView.as_view(), name="models_overview"),
    path("models/<int:pk>/", views.ModelView.as_view(), name="model_view"),
    path("submit", views.submit, name="model_submission"),
    path("contact", views.contact, name="contact_page"),
    path("account/register", views.register_request, name="register"),
    # path("login", views.login_request, name="login"),
    # path("logout", views.logout_request, name="logout"),
    path("submit_anon/", views.submit_anon, name="submit_anon"),
]
