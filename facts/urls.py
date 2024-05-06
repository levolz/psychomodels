from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="facts_index"),
    path("phenomena/", views.PhenomenaView.as_view(), name="phenomena"),
    path("phenomena/<int:pk>/", views.PhenomenonView.as_view(), name="phenomenon_view"),
    path("constructs/", views.ConstructsView.as_view(), name="constructs"),
    path("constructs/<int:pk>/", views.ConstructView.as_view(), name="construct_view"),
    path("patterns/", views.PatternsView.as_view(), name="patterns"),
    path("patterns/<int:pk>/", views.PatternView.as_view(), name="pattern_view"),
]
