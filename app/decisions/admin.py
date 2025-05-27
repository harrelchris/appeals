from django.contrib import admin

from .models import URL, Decision, DecisionMeta, Condition


class ConditionAdmin(admin.ModelAdmin):
    pass


class DecisionAdmin(admin.ModelAdmin):
    pass


class DecisionMetaAdmin(admin.ModelAdmin):
    pass


class URLAdmin(admin.ModelAdmin):
    pass


admin.site.register(Condition, ConditionAdmin)
admin.site.register(Decision, DecisionAdmin)
admin.site.register(DecisionMeta, DecisionMetaAdmin)
admin.site.register(URL, URLAdmin)
