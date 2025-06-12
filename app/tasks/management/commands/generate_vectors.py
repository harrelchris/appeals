from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from decisions.models import Decision
from tasks.models import Task

TASK_NAME = "generate-vectors"


class Command(BaseCommand):
    help = "Generate vectors for the decision text."

    def handle(self, *args, **options):
        qs = Decision.objects.filter(vector=None)
        count = qs.count()

        qs.update(vector=SearchVector("text"))

        task = Task(name=TASK_NAME, success=True)
        task.save()

        message = f"Generated {count} vectors."
        self.stdout.write(self.style.SUCCESS(message))
