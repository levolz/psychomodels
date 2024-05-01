from django.db import models
from markdownx.models import MarkdownxField
from models.models import Psychfield, Behaviour, Variable, Publication


class Construct(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1500, null=True, blank=True)
    field = models.ForeignKey(
        Psychfield, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    variables = models.ManyToManyField(Variable, blank=True)

    def __str__(self):
        return self.name


class Pattern(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1500, null=True, blank=True)
    # behaviour = models.ForeignKey(Behaviour, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name


class Evidence(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1500, null=True, blank=True)
    publication = models.ForeignKey(Publication, on_delete=models.DO_NOTHING, null=True)
    data = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Phenomenon(models.Model):
    publication = models.ForeignKey(
        Publication, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    name = models.CharField(max_length=200)
    short = models.CharField(max_length=500, null=True, blank=True)
    description = MarkdownxField(max_length=3000, null=True, blank=True)
    field = models.ManyToManyField(Psychfield, blank=True)
    constructs = models.ManyToManyField(Construct, blank=True)

    def __str__(self):
        return self.name


class Fact(models.Model):
    phenomenon = models.ForeignKey(
        Phenomenon, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    name = models.CharField(max_length=200)
    short = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=1500, null=True, blank=True)
    patterns = models.ManyToManyField(Pattern, blank=True)
    evidence = models.ManyToManyField(Evidence, blank=True)

    def __str__(self):
        return self.name
