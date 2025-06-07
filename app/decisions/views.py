from django.views.generic import DetailView

from decisions.models import Decision


class DecisionDetailView(DetailView):
    template_name = "decisions/detail.html"
    model = Decision
    context_object_name = "decision"
