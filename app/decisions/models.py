from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.db import models

OUTCOMES = [
    ("granted", "granted"),
    ("denied", "denied"),
    ("remanded", "remanded"),
]


class URL(models.Model):
    loc = models.CharField(max_length=128, unique=True)
    lastmod = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.loc


class Decision(models.Model):
    text = models.TextField()
    vector = SearchVectorField(null=True)
    citation = models.CharField(max_length=128, null=True, blank=True)
    date = models.CharField(max_length=10, null=True, blank=True)
    docket = models.CharField(max_length=128, null=True, blank=True)
    judge = models.CharField(max_length=128, null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    url = models.ForeignKey(URL, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            GinIndex(fields=["vector"]),
        ]

    def __str__(self) -> str:
        return f"{self.text[:100]}..."

    def save(self, *args, **kwargs):
        self.vector = SearchVector("text")
        super().save(*args, **kwargs)


class Condition(models.Model):
    name = models.CharField(max_length=1024)
    outcome = models.CharField(max_length=10, choices=OUTCOMES, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} > {self.outcome}"
