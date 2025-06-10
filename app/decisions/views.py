from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchRank, SearchVector
from django.db.models import F

from decisions.models import Decision


class DecisionDetailView(DetailView):
    template_name = "decisions/detail.html"
    model = Decision
    context_object_name = "decision"


class DecisionListView(ListView):
    template_name = "decisions/list.html"
    model = Decision
    context_object_name = "decisions"
    paginate_by = 50
    ordering = "-date"


class DecisionSearchView(TemplateView):
    template_name = "decisions/search.html"


class DecisionResultsView(ListView):
    template_name = "decisions/list.html"
    model = Decision
    context_object_name = "decisions"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        query = SearchQuery(
            value=q,
            search_type="websearch",
        )
        headline = SearchHeadline(
            expression=F("text"),
            query=query,
            start_sel="<mark>",
            stop_sel="</mark>",
        )
        return (
            Decision.objects
            .annotate(rank=SearchRank(F("vector"), query))  # use precomputed vector field
            .annotate(headline=headline)
            .filter(rank__gte=0.001)
            .order_by("-rank")
        )
