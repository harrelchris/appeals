from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from decisions.models import Decision


class Command(BaseCommand):
    help = "Populate or update the search_vector field for full-text search"

    def handle(self, *args, **options):
        qs = Decision.objects.filter(vector=None)
        count = qs.count()

        self.stdout.write(f"Updating search_vector for {count} decisions...")

        for decision in qs:
            decision.vector = SearchVector("text")
            decision.save()

        self.stdout.write(self.style.SUCCESS("Done updating search_vector field."))
