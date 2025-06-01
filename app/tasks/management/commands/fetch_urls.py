import sys

import bs4
from django.core.management.base import BaseCommand
import requests

from decisions.models import URL
from tasks.models import Task

TASK_NAME = "fetch-urls"


class Command(BaseCommand):
    help = "Fetch new URLs"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_run_date = None

    def handle(self, *args, **options):
        msg = "Fetching new URLs"
        self.stdout.write(self.style.SUCCESS(msg))

        self.last_run_date = self.get_last_run_date()
        updated_sitemaps = self.get_updated_sitemaps()
        updated_urls = []
        for sitemap in updated_sitemaps:
            urls = self.get_updated_urls(sitemap["loc"])
            updated_urls.extend(urls)

        existing_urls = set(URL.objects.values_list("loc", flat=True))
        new_urls = [u for u in updated_urls if u["loc"] not in existing_urls]

        msg = f"{len(new_urls)} new URLs found."
        self.stdout.write(self.style.SUCCESS(msg))

        records = [URL(**u) for u in new_urls]
        URL.objects.bulk_create(records)

        task = Task(name=TASK_NAME, success=True)
        task.save()

    @classmethod
    def get_last_run_date(cls) -> str:
        task = Task.objects.filter(name=TASK_NAME, success=True).order_by("-datetime").first()
        if not task:
            return "1970-01-01"
        return task.datetime.strftime("%Y-%m-%d")

    def get_updated_sitemaps(self) -> list[dict[str, str]]:
        soup = self.request_xml_soup("https://www.va.gov/sitemap_bva.xml")
        sitemap_index = soup.find("sitemapindex")
        elements = sitemap_index.find_all("sitemap")
        updated_elements = self.extract_updated_elements(elements)
        return updated_elements

    def get_updated_urls(self, url: str) -> list[dict[str, str]]:
        soup = self.request_xml_soup(url)
        url_set = soup.find("urlset")
        elements = url_set.find_all("url")
        updated_elements = self.extract_updated_elements(elements)
        return updated_elements

    @classmethod
    def request_xml_soup(cls, url: str) -> bs4.BeautifulSoup:
        response = requests.get(url)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            task = Task(name=TASK_NAME, success=False)
            task.save()
            sys.exit(1)

        content = response.content.decode("utf-8")
        return bs4.BeautifulSoup(content, "lxml-xml")

    def extract_updated_elements(self, elements: bs4.ResultSet) -> list[dict[str, str]]:
        children = []
        for element in elements:
            children.append({
                "loc": element.find("loc").text,
                "lastmod": element.find("lastmod").text,
            })
        updated_children = [c for c in children if c["lastmod"] > self.last_run_date]
        return updated_children
