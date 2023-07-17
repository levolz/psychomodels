from django.contrib import admin

# Register your models here.
from . import models


class PublicationAdmin(admin.ModelAdmin):
    filter_horizontal = ["model_authors"]


class FrameworkAdmin(admin.ModelAdmin):
    filter_horizontal = ["frameworks"]


admin.site.register(models.Author)
admin.site.register(models.Psychmodel)
# admin.site.register(models.Parameter)
admin.site.register(models.Modelparameter)
# admin.site.register(models.Variable)
admin.site.register(models.Modelvariable)
admin.site.register(models.Language)
admin.site.register(models.Framework)
# admin.site.register(models.Psychfield)
admin.site.register(models.Publication, PublicationAdmin)
# admin.site.register(models.Softwarepackage)
# admin.site.register(models.Measurementinstrument)
