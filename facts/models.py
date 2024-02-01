from django.db import models
from models.models import Psychfield


class phenomenon(models.Model):
    phenomenon_name = models.CharField(max_length=200)
    phenomenon_description = models.CharField(max_length=1500)
    psychfield = models.ForeignKey(Psychfield, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.phenomenon_name
