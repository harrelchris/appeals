from django.core.management.base import BaseCommand

from decisions.models import Decision
from tasks.models import Task

TASK_NAME = "extract_citations"


def extract(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines:
        line_lower = line.lower()
        if line_lower.startswith("citation nr: "):
            parts = line.split(": ")
            if len(parts) == 2:
                return parts[1].strip()
    return None


class Command(BaseCommand):
    help = "Extract citation from decision text"

    def handle(self, *args, **options):
        qs = Decision.objects.filter(citation=None)
        decisions = []
        for decision in qs:
            decision.citation = extract(decision.text)
            decisions.append(decision)
        Decision.objects.bulk_update(decisions, ["citation"])

        task = Task(name=TASK_NAME, success=True)
        task.save()

        message = f"Extracted {len(decisions)} citations."
        self.stdout.write(self.style.SUCCESS(message))
