from django.db import models


class PsychmodelManager(models.Manager):
    def create_model(
        self,
        title,
        description,
        publication,
        # authors,
        # frameworks,
        # softwarepackages,
        # languages,
        # model_file,
    ):
        model = self.create(
            title=title,
            description=description,
            publication=publication,
            # =model_file,
        )

        # for author in authors:
        #    model.author_set.add(author)

        # for framework in frameworks:
        #    model.framework_set.add(framework)
