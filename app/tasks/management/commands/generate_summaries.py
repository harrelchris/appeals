from django.core.management.base import BaseCommand
from decisions.models import Decision
from tasks.models import Task
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.utils import get_stop_words

TASK_NAME = "summarize-decisions"
LANGUAGE = "english"
SENTENCES_COUNT = 10

stemmer = Stemmer(LANGUAGE)
summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)


def summarize(text):
    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    sentences = summarizer(parser.document, SENTENCES_COUNT)
    return "\n".join([str(s) for s in sentences])


class Command(BaseCommand):
    help = "Summarize the text of each decision"

    def handle(self, *args, **options):
        qs = Decision.objects.filter(summary=None)
        count = qs.count()
        decisions = list(qs)

        self.stdout.write(f"Updating summary field for {count} decisions...")

        for decision in decisions:
            decision.summary = summarize(decision.text)

        Decision.objects.bulk_update(decisions, ["summary"])

        self.stdout.write(self.style.SUCCESS("Done updating summary field."))

        task = Task(name=TASK_NAME, success=True)
        task.save()
