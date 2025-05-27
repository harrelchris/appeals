from django.db import models

from django.utils import timezone


class Task(models.Model):
    name = models.CharField(max_length=64, editable=False)
    datetime = models.DateTimeField(default=timezone.now)
    success = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.datetime.strftime("%Y-%M-%d %H:%M:%S")}] {'SUCCESS' if self.success else 'ERROR'} {self.name}"
