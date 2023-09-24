import logging
from datetime import date
from random import choice
from string import ascii_uppercase, digits

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F
from rest_framework.exceptions import ValidationError

from ad.models import Ads
from booking.dataclasses import BookingPriceTotal
from vendor.mixins.model import ModelWithoutIdMixin
from vendor.validators import not_date_past


def random_string() -> str:
    return ''.join(choice(ascii_uppercase + digits) for _ in range(16)).upper()


class Booking(ModelWithoutIdMixin):

    code = models.CharField(max_length=16,
                            primary_key=True,
                            default=random_string,
                            editable=False,
                            verbose_name="código do Booking")
    ad = models.ForeignKey(Ads,
                           on_delete=models.CASCADE,
                           blank=False,
                           null=False,
                           verbose_name="Anúncio")
    check_in = models.DateField(blank=False,
                                null=False,
                                default=date.today,
                                verbose_name="CheckIn",
                                validators=[not_date_past])
    check_out = models.DateField(blank=False,
                                 null=False,
                                 default=date.today,
                                 verbose_name="CheckOut",
                                 validators=[not_date_past])
    total_price = models.FloatField(blank=False,
                                    editable=False,
                                    null=False,
                                    default=0.0,
                                    verbose_name='Preço total')
    comment = models.TextField(blank=False,
                               null=True,
                               verbose_name="Comentário")
    number_guests = models.IntegerField(default=1,
                                        blank=False,
                                        null=False,
                                        verbose_name="Número de hóspedes",
                                        validators=[
                                            MaxValueValidator(100),
                                            MinValueValidator(1)
                                        ])

    def _set_price_total(self):
        logging.info(f"{self.ad.uuid}")
        result = (Ads.objects
                  .select_related("property")
                  .filter(pk=self.ad.uuid)
                  .annotate(cleaning_cost=F('property__cleaning_cost'))
                  .values('cleaning_cost', 'platform_rate')
                  .first())
        if result:
            booking_price_total = BookingPriceTotal(**result)
            self.total_price = (booking_price_total.platform_rate * (self.check_out - self.check_in).days)
            self.total_price = self.total_price + booking_price_total.cleaning_cost
        else:
            raise ValidationError('Erro Interno, entre em contato com o suporte.')

    def _number_guests_gather_than(self):
        ad: Ads = Ads.objects.get(pk=self.ad.uuid)
        if ad:
            if self.number_guests > ad.property.guest_limit:
                raise ValidationError(f"Número hospedes superior ao disponível pelo "
                                      f"imóvel, sendo, {self.number_guests} > {ad.property.guest_limit}")

    def save(self, *args, **kwargs):
        if self.check_out == self.check_in:
            raise ValidationError("O CheckOut não pode ser igual a data de CheckIn")
        elif self.check_out < self.check_in:
            raise ValidationError("O CheckOut não pode ser menor que a data de CheckIn")
        elif self.check_in > self.check_out:
            raise ValidationError("O CheckIn não pode ser maior que a data de Checkout")
        elif self.check_in < date.today() or self.check_out < date.today():
            raise ValidationError("O CheckIn ou CheckOut não pode ser menor que a data atual")
        if Booking.objects.filter(check_in=self.check_in, check_out=self.check_out, ad=self.ad).exists():
            raise ValidationError("Data indisponível para reservar, tente outro intervalo de datas")

        self._set_price_total()
        self._number_guests_gather_than()
        super(Booking, self).save(*args, **kwargs)

    class Meta:
        ordering = ['code', 'check_in', 'check_out', 'ad', 'number_guests', 'total_price']
        verbose_name = "booking"
        verbose_name_plural = "booking"
