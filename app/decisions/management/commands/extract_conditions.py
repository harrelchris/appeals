from django.core.management.base import BaseCommand, CommandError

from decisions.models import Condition
from tasks.models import Task


class Command(BaseCommand):
    help = "Extract Conditions"

    def handle(self, *args, **options):
        task = Task(
            name="extract_conditions",
            success=True,
        )
        task.save()
        msg = "Extracting Conditions"
        self.stdout.write(self.style.SUCCESS(msg))
