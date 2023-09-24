from django.core.validators import MinValueValidator
from django.db import models

from vendor.mixins.model import ModelMixin
from property.models import Property


class Ads(ModelMixin):
    property = models.ForeignKey(Property,
                                 on_delete=models.CASCADE,
                                 blank=False,
                                 null=False,
                                 verbose_name="UUID do Imóvel")
    platform = models.CharField(max_length=256,
                                blank=False,
                                null=False,
                                verbose_name='Nome da plataforma')
    platform_rate = models.FloatField(blank=False,
                                      null=False,
                                      default=0.0,
                                      validators=[
                                          MinValueValidator(0)
                                      ],
                                      verbose_name="Taxa da plataforma")

    class Meta:
        ordering = ['uuid', 'property', 'platform', 'platform_rate']
        verbose_name = "ad"
        verbose_name_plural = "ads"
