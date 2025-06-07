from django.urls import path

from . import views

app_name = "decisions"

urlpatterns = [
    path("<int:pk>/", views.DecisionDetailView.as_view(), name="detail"),
]
