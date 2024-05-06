from django.contrib import admin
from . import models

admin.site.register(models.Phenomenon)
admin.site.register(models.Construct)
admin.site.register(models.Pattern)
admin.site.register(models.Evidence)
admin.site.register(models.Fact)
