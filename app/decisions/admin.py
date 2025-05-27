from django.contrib import admin

from .models import URL, Condition, Decision, DecisionMeta


class ConditionAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "outcome",
        "reason",
    ]
    list_filter = [
        "name",
        "outcome",
    ]


class DecisionAdmin(admin.ModelAdmin):
    pass


class DecisionMetaAdmin(admin.ModelAdmin):
    list_display = [
        "citation",
        "date",
        "docket",
        "judge",
    ]


class URLAdmin(admin.ModelAdmin):
    list_display = [
        "loc",
        "lastmod",
    ]
    list_filter = [
        "lastmod",
    ]


admin.site.register(Condition, ConditionAdmin)
admin.site.register(Decision, DecisionAdmin)
admin.site.register(DecisionMeta, DecisionMetaAdmin)
admin.site.register(URL, URLAdmin)
