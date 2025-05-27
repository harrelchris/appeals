from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "success",
        "datetime",
    ]
    list_filter = [
        "name",
        "success",
        "datetime",
    ]


admin.site.register(Task, TaskAdmin)
