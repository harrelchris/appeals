import sqlite3

from django.core.management.base import BaseCommand

from decisions.models import URL, Decision

SOURCE_DATABASE_URL = "/Users/chris/Dev/appeals-data/db.sqlite3"


class Command(BaseCommand):
    def handle(self, *args, **options):
        msg = "Migrating Decisions"
        self.stdout.write(self.style.SUCCESS(msg))

        conn = sqlite3.connect(SOURCE_DATABASE_URL)
        c = conn.cursor()

        chunk_size = 1_000
        for i in range(0, 1_770_000, chunk_size):
            stmt = f"SELECT url, text FROM decision WHERE id BETWEEN {i} AND {i + chunk_size};"
            c.execute(stmt)
            rows = c.fetchall()
            decisions = []
            for row in rows:
                url = URL.objects.get(loc=row[0])
                decision = Decision(
                    url=url,
                    text=row[1],
                )
                decisions.append(decision)
            Decision.objects.bulk_create(decisions)
            msg = f"Migrated {i} - {i + chunk_size}"
            self.stdout.write(self.style.SUCCESS(msg))
