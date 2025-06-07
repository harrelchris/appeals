from django.urls import path

from . import views

app_name = "decisions"

urlpatterns = [
    path("", view=views.DecisionListView.as_view(), name="list"),
    path("search/", view=views.DecisionSearchView.as_view(), name="search"),
    path("results/", view=views.DecisionResultsView.as_view(), name="results"),
    path("<int:pk>/", views.DecisionDetailView.as_view(), name="detail"),
]
