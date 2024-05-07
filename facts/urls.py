from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="facts_index"),
    path("phenomena/", views.PhenomenaView.as_view(), name="phenomena"),
    path("phenomena/<int:pk>/", views.PhenomenonView.as_view(), name="phenomenon_view"),
    path("constructs/", views.ConstructsView.as_view(), name="constructs"),
    path("constructs/<int:pk>/", views.ConstructView.as_view(), name="construct_view"),
    path("facts/", views.FactsView.as_view(), name="facts"),
    path("facts/<int:pk>/", views.FactView.as_view(), name="fact_view"),
]
