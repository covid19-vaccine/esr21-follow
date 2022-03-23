from django.db import models

from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_call_manager.model_mixins import (
    CallModelMixin, LogModelMixin, LogEntryModelMixin)

from ..choices import CONTACT_FAIL_REASON, CALL_STATUS


class ESRCallManager(models.Manager):

    def get_by_natural_key(self, subject_identifier, visit_code):
        return self.get(subject_identifier=subject_identifier,
                        visit_code=visit_code)


class Call(CallModelMixin, BaseUuidModel):

    scheduled = models.DateTimeField(
        default=get_utcnow)

    visit_code = models.CharField(
        max_length=25,
        null=True,
        editable=False)

    objects = ESRCallManager()

    def natural_key(self):
        return (self.subject_identifier, self.visit_code)

    class Meta(CallModelMixin.Meta):
        app_label = 'esr21_follow'
        unique_together = ('subject_identifier', 'visit_code',)


class Log(LogModelMixin, BaseUuidModel):

    call = models.ForeignKey(Call, on_delete=models.PROTECT)

    def natural_key(self):
        return (self.log_datetime, self.call.subject_identifier, self.call.label,
                self.call.scheduled)

    class Meta(LogModelMixin.Meta):
        app_label = 'esr21_follow'


class LogEntry(LogEntryModelMixin, BaseUuidModel):

    log = models.ForeignKey(Log, on_delete=models.PROTECT)

    call_status = models.CharField(
        max_length=50,
        choices=CALL_STATUS,
        default='successful')

    reason_unsuccesful = models.CharField(
        verbose_name='Reasons call unsuccessful?',
        max_length=150,
        choices=CONTACT_FAIL_REASON,
        null=True,
        blank=True)

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        null=True,
        blank=True)

    comment = models.TextField(
        verbose_name='Comments',
        null=True,
        blank=True)

    class Meta(LogEntryModelMixin.Meta):
        app_label = 'esr21_follow'

