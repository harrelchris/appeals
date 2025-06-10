from django.core.management.base import BaseCommand

from decisions.models import Decision
from tasks.models import Task

TASK_NAME = "extract_judge"


def extract(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for index, line in enumerate(lines):
        line_lower = line.lower()
        if line_lower in ("veterans law judge", "acting veterans law judge"):
            return lines[index - 1]
    return None


class Command(BaseCommand):
    help = "Extract judge from decision text"

    def handle(self, *args, **options):
        qs = Decision.objects.filter(judge=None)
        decisions = []
        for decision in qs:
            decision.judge = extract(decision.text)
            decisions.append(decision)
        Decision.objects.bulk_update(decisions, ["judge"])

        task = Task(name=TASK_NAME, success=True)
        task.save()

        message = f"Extracted {len(decisions)} judges."
        self.stdout.write(self.style.SUCCESS(message))
