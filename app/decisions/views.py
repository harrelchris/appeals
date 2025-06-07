from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.postgres.search import SearchHeadline, SearchQuery, SearchRank, SearchVector

from decisions.models import Decision


class DecisionDetailView(DetailView):
    template_name = "decisions/detail.html"
    model = Decision
    context_object_name = "decision"


class DecisionListView(ListView):
    template_name = "decisions/list.html"
    model = Decision
    context_object_name = "decisions"
    paginate_by = 100


class DecisionSearchView(TemplateView):
    template_name = "decisions/search.html"


class DecisionResultsView(ListView):
    template_name = "decisions/list.html"
    model = Decision
    context_object_name = "decisions"
    paginate_by = 100

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        vector = SearchVector("text")  # can include multiple columns: SearchVector("text", "title")
        query = SearchQuery(q)
        headline = SearchHeadline("text", query)

        # return Decision.objects.filter(text__search=q)
        # return Decision.objects.annotate(search=vector).filter(search=query)
        # return Decision.objects.annotate(rank=SearchRank(vector, query)).order_by("-rank")
        # return Decision.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.001).order_by("-rank")
        return Decision.objects.annotate(rank=SearchRank(vector, query)).annotate(headline=headline).filter(rank__gte=0.001).order_by("-rank")
