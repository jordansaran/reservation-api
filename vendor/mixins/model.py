import uuid
from django.db import models


class ModelMixin(models.Model):
    """
    Abstract create and update dates class
    """
    uuid = models.CharField(primary_key=True,
                            max_length=36,
                            default=uuid.uuid4,
                            editable=False,
                            verbose_name="uuid")
    created_at = models.DateTimeField(editable=False,
                                      auto_now_add=True,
                                      verbose_name="Data de criação",
                                      blank=False,
                                      null=False)
    updated_at = models.DateTimeField(editable=False,
                                      auto_now=True,
                                      verbose_name="Data de atualização",
                                      blank=False,
                                      null=False)

    class Meta:
        abstract = True


class ModelWithoutIdMixin(models.Model):
    """
    Abstract create and update dates class
    """
    created_at = models.DateTimeField(editable=False,
                                      auto_now_add=True,
                                      verbose_name="Data de criação",
                                      blank=False,
                                      null=False)
    updated_at = models.DateTimeField(editable=False,
                                      auto_now=True,
                                      verbose_name="Data de atualização",
                                      blank=False,
                                      null=False)

    class Meta:
        abstract = True