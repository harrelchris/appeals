from django.core.management.base import BaseCommand, CommandError

from decisions.models import URL
from tasks.models import Task


class Command(BaseCommand):
    help = "Fetch new URLs"

    def handle(self, *args, **options):
        msg = "Fetching new URLs"
        self.stdout.write(self.style.SUCCESS(msg))
