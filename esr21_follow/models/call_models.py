from django.db import models

from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow

from edc_call_manager.model_mixins import (
    CallModelMixin, LogModelMixin, LogEntryModelMixin)


class Call(CallModelMixin, BaseUuidModel):

    scheduled = models.DateTimeField(
        default=get_utcnow)

    visit_code = models.CharField(
        max_length=25,
        null=True,
        editable=False)

    class Meta(CallModelMixin.Meta):
        app_label = 'esr21_follow'
        unique_together = ('subject_identifier', 'visit_code',)


class Log(LogModelMixin, BaseUuidModel):

    call = models.ForeignKey(Call, on_delete=models.PROTECT)

    class Meta(LogModelMixin.Meta):
        app_label = 'esr21_follow'


class LogEntry(LogEntryModelMixin, BaseUuidModel):

    log = models.ForeignKey(Log, on_delete=models.PROTECT)

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        null=True,
        blank=True)

    class Meta(LogEntryModelMixin.Meta):
        app_label = 'esr21_follow'

