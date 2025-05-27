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
    url = models.ForeignKey(URL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.text[:100]}..."


class DecisionMeta(models.Model):
    class Meta:
        verbose_name_plural = "decision metadata"

    citation = models.CharField(max_length=128, null=True, blank=True)
    date = models.CharField(max_length=10, null=True, blank=True)
    docket = models.CharField(max_length=128, null=True, blank=True)
    judge = models.CharField(max_length=128, null=True, blank=True)
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.citation


class Condition(models.Model):
    name = models.CharField(max_length=1024)
    outcome = models.CharField(max_length=10, choices=OUTCOMES, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} > {self.outcome}"
