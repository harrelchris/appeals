from django.core.management.base import BaseCommand

from decisions.models import Decision
from tasks.models import Task

TASK_NAME = "extract_date"


def extract(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines:
        line_lower = line.lower()
        if line_lower.startswith("decision date: "):
            if "archive date: " in line_lower:
                if "\t" in line_lower:
                    parts = line_lower.split("\t")
                    decision_date_str, archive_date_str = parts
                    decision_date = decision_date_str.split(": ")[1].strip()
                    archive_date = archive_date_str.split(": ")[1].strip()
                    return decision_date or archive_date
    return None


class Command(BaseCommand):
    help = "Extract date from decision text"

    def handle(self, *args, **options):
        qs = Decision.objects.filter(date=None)
        decisions = []
        for decision in qs:
            decision.date = extract(decision.text)
            decisions.append(decision)
        Decision.objects.bulk_update(decisions, ["date"])

        task = Task(name=TASK_NAME, success=True)
        task.save()

        message = f"Extracted {len(decisions)} dates."
        self.stdout.write(self.style.SUCCESS(message))
