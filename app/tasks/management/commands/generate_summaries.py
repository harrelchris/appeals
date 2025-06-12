from django.core.management.base import BaseCommand
from decisions.models import Decision
from tasks.models import Task
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.utils import get_stop_words
from numpy.linalg import LinAlgError

TASK_NAME = "generate_summaries"
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

        try:
            for decision in decisions:
                decision.summary = summarize(decision.text)
        except LinAlgError:
            message = f"Generated {count} summaries."
            self.stdout.write(self.style.SUCCESS(message))
            task = Task(name=TASK_NAME, success=False)
            task.save()
        else:
            Decision.objects.bulk_update(decisions, ["summary"])

            task = Task(name=TASK_NAME, success=True)
            task.save()

            message = f"Generated {count} summaries."
            self.stdout.write(self.style.SUCCESS(message))
