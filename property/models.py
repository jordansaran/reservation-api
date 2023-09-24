from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from vendor.mixins.model import ModelMixin
from vendor.validators import not_date_past


class Property(ModelMixin):

    guest_limit = models.SmallIntegerField(blank=False,
                                           null=False,
                                           default=1,
                                           verbose_name="Limite de hóspedes",
                                           validators=[
                                               MaxValueValidator(100),
                                               MinValueValidator(1)
                                           ])
    number_bathrooms = models.SmallIntegerField(blank=False,
                                                null=False,
                                                default=0,
                                                verbose_name="Quantidade de banheiros",
                                                validators=[
                                                    MaxValueValidator(100),
                                                    MinValueValidator(0)
                                                ])
    pets_allowed = models.BooleanField(blank=False,
                                       null=False,
                                       default=False,
                                       verbose_name="Animais de estimação é permitido?")
    cleaning_cost = models.FloatField(blank=False,
                                      null=False,
                                      default=0.0,
                                      validators=[
                                          MinValueValidator(0.0)
                                      ],
                                      verbose_name="Valor da limpeza")
    activation_date = models.DateField(blank=False,
                                       null=False,
                                       default=date.today,
                                       verbose_name="Data de ativação do imóvel",
                                       validators=[not_date_past])

    def save(self, *args, **kwargs):
        if self.activation_date < date.today():
            raise ValidationError("A data não pode ser menor que a data atual.")
        super(Property, self).save(*args, **kwargs)

    class Meta:
        ordering = ['activation_date', 'guest_limit', 'pets_allowed', 'cleaning_cost']
        verbose_name = "property"
        verbose_name_plural = "properties"
