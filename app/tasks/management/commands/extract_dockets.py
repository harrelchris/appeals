from django.core.management.base import BaseCommand

from decisions.models import Decision
from tasks.models import Task

TASK_NAME = "extract_docket"


def extract(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines:
        line_lower = line.lower()
        if line_lower.startswith("docket no. "):
            parts = line_lower.split(". ")
            return parts[1].strip()
    return None


class Command(BaseCommand):
    help = "Extract docket from decision text"

    def handle(self, *args, **options):
        qs = Decision.objects.filter(docket=None)
        decisions = []
        for decision in qs:
            decision.docket = extract(decision.text)
            decisions.append(decision)
        Decision.objects.bulk_update(decisions, ["docket"])

        task = Task(name=TASK_NAME, success=True)
        task.save()

        message = f"Extracted {len(decisions)} dockets."
        self.stdout.write(self.style.SUCCESS(message))
