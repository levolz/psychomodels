from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from markdownx.widgets import AdminMarkdownxWidget

# Register your models here.
from . import models


class PublicationAdmin(admin.ModelAdmin):
    filter_horizontal = ["authors"]


class PsychmodelAdmin(admin.ModelAdmin):
    list_display = ["model_name", "reviewed"]
    filter_horizontal = ["framework"]

    actions = ["mark_as_reviewed", "mark_as_unreviewed"]

    @admin.action(description="Mark selected models as reviewed")
    def mark_as_reviewed(self, request, queryset):
        queryset.update(reviewed=True)
        self.message_user(request, "The selected models have been marked as reviewed.")

    @admin.action(description="Mark selected models as unreviewed")
    def mark_as_unreviewed(self, request, queryset):
        queryset.update(reviewed=False)
        self.message_user(
            request, "The selected models have been marked as unreviewed."
        )


admin.site.register(models.Author)
admin.site.register(models.Psychmodel, PsychmodelAdmin)
admin.site.register(models.Proposal)
admin.site.register(models.Variable)
admin.site.register(models.Modelvariable)
admin.site.register(models.Language)
admin.site.register(models.Framework, MarkdownxModelAdmin)
admin.site.register(models.Psychfield)
admin.site.register(models.Publication, PublicationAdmin)
admin.site.register(models.Softwarepackage)
admin.site.register(models.Measurementinstrument)
