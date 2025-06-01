from concurrent.futures import as_completed

from django.core.management.base import BaseCommand
from requests_futures.sessions import FuturesSession

from decisions.models import URL, Decision
from tasks.models import Task

TASK_NAME = "fetch-decisions"

session = FuturesSession()


class Command(BaseCommand):
    help = "Fetch new Decisions"

    def handle(self, *args, **options):
        msg = "Fetching new Decisions"
        self.stdout.write(self.style.SUCCESS(msg))

        urls = URL.objects.exclude(id__in=Decision.objects.values("url_id"))
        url_list = list(urls)
        chunk_size = 100
        url_chunks = [url_list[i : i + chunk_size] for i in range(0, len(url_list), chunk_size)]

        for chunk in url_chunks:
            start = chunk[0].id
            stop = chunk[-1].id
            msg = f"Requesting decisions: {start} - {stop}"
            self.stdout.write(self.style.SUCCESS(msg))

            futures = []
            for url in chunk:
                future = session.get(url.loc)
                future.url = url
                futures.append(future)

            decisions = []
            for future in as_completed(futures):
                response = future.result()
                decision = Decision(
                    url=future.url,
                    text=response.text,
                )
                decisions.append(decision)

            decisions = sorted(decisions, key=lambda d: d.url_id)
            Decision.objects.bulk_create(decisions)

        task = Task(name=TASK_NAME, success=True)
        task.save()
