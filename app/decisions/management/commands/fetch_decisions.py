from django.core.management.base import BaseCommand, CommandError

from decisions.models import Decision
from tasks.models import Task


class Command(BaseCommand):
    help = "Fetch new Decisions"

    def handle(self, *args, **options):
        msg = "Fetching new Decisions"
        self.stdout.write(self.style.SUCCESS(msg))
