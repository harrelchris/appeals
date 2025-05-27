from django.core.management.base import BaseCommand, CommandError

from decisions.models import Decision
from tasks.models import Task


class Command(BaseCommand):
    help = "Extract Decision Metadata"

    def handle(self, *args, **options):
        msg = "Extracting Decision Metadata"
        self.stdout.write(self.style.SUCCESS(msg))
