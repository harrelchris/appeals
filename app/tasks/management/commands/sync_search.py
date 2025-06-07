import json

from django.core.management.base import BaseCommand
import meilisearch
from django.db.models import Max
from django.conf import settings

from decisions.models import Decision

client = meilisearch.Client(settings.MEILI_HTTP_ADDR, settings.MEILI_MASTER_KEY)


class Command(BaseCommand):
    help = "Sync search index with database"

    def handle(self, *args, **options):
        msg = "Syncing Search"
        self.stdout.write(self.style.SUCCESS(msg))

        max_id = Decision.objects.all().aggregate(Max('id'))['id__max']

        chunk_size = 1000
        for i in range(0, max_id, chunk_size):
            decisions = Decision.objects.filter(id__range=(i, i+chunk_size)).values("id", "text")
            decisions = list(decisions)
            client.index("decisions").add_documents(decisions)

            msg = f"{i} - {i + chunk_size} synced"
            self.stdout.write(self.style.SUCCESS(msg))


# meilisearch.errors.MeilisearchApiError: MeilisearchApiError. Error code: payload_too_large. Error message: The provided payload reached the size limit. The maximum accepted payload size is 95.367431640625 MiB. Error documentation: https://docs.meilisearch.com/errors#payload_too_large Error type: invalid_request
