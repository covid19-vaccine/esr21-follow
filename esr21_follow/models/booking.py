from django.db import models

from django_crypto_fields.fields import EncryptedCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import CellNumber
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_search.model_mixins import SearchSlugModelMixin, SearchSlugManager


class BookingManager(SearchSlugManager, models.Manager):
    pass


class Booking(SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):

    first_name = models.CharField(
        verbose_name='First name',
        max_length=250,
        null=True)

    middle_name = models.CharField(
        verbose_name='Middle name',
        max_length=250,
        null=True)

    last_name = models.CharField(
        verbose_name='Last name',
        max_length=250,
        null=True)

    subject_cell = EncryptedCharField(
       verbose_name='Mobile phone number',
       validators=[CellNumber, ],
       unique=True,
       blank=True,
       null=True,)

    booking_date = models.DateField(
        verbose_name="Booking date",
        null=True,
    )

    successful = models.BooleanField(default=False)

    objects = BookingManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def natural_key(self):
        return (self.cell_number, )

    def get_search_slug_fields(self):
        fields = ['cell_number']
        return fields

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'esr21_follow'
        verbose_name = 'Booking'
