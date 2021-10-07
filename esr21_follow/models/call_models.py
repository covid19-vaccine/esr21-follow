from django.db import models
from multiselectfield import MultiSelectField

from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_is_future, datetime_not_future
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, NOT_APPLICABLE

from edc_call_manager.model_mixins import (
    CallModelMixin, LogModelMixin)

from ..choices import (
    APPT_GRADING, APPT_LOCATIONS,
    CONTACT_FAIL_REASON, PHONE_USED, PHONE_SUCCESS, YES_NO_ST_NA)
from .list_models import ReasonsUnwilling


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


class LogEntry(BaseUuidModel):

    log = models.ForeignKey(Log, on_delete=models.PROTECT)

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        null=True,
        blank=True)

    call_datetime = models.DateTimeField(
        default=get_utcnow,
        validators=[datetime_not_future, ],
        verbose_name='Date of contact attempt')

    phone_num_type = MultiSelectField(
        verbose_name='Which phone number(s) was used for contact?',
        choices=PHONE_USED)

    phone_num_success = MultiSelectField(
        verbose_name='Which number(s) were you successful in reaching?',
        choices=PHONE_SUCCESS)

    cell_contact_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    alt_cell_contact_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    tel_contact_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    alt_tel_contact_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    work_contact_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    cell_alt_contact_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    tel_alt_contact_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    cell_resp_person_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    tel_resp_person_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    appt = models.CharField(
        verbose_name='Is the participant willing to schedule an appointment',
        max_length=10,
        choices=YES_NO_ST_NA,
        default=NOT_APPLICABLE)

    appt_reason_unwilling = models.ManyToManyField(
        ReasonsUnwilling,
        verbose_name=('What is the reason the participant is unwilling to '
                      'schedule an appointment'),
        blank=True)

    appt_reason_unwilling_other = models.CharField(
        verbose_name='Other reason, please specify ...',
        max_length=50,
        null=True,
        blank=True)

    appt_date = models.DateField(
        verbose_name="Appointment Date",
        validators=[date_is_future],
        null=True,
        blank=True,
        help_text="This can only come from the participant.")

    appt_grading = models.CharField(
        verbose_name='Is this appointment...',
        max_length=25,
        choices=APPT_GRADING,
        null=True,
        blank=True)

    appt_location = models.CharField(
        verbose_name='Appointment location',
        max_length=50,
        choices=APPT_LOCATIONS,
        null=True,
        blank=True)

    appt_location_other = OtherCharField(
        verbose_name='Other location, please specify ...',
        max_length=50,
        null=True,
        blank=True)

    @property
    def subject(self):
        """Override to return the FK attribute to the subject.

        expects any model instance with fields ['first_name', 'last_name', 'gender', 'dob'].

        For example: self.registered_subject.

        See also: CallSubjectViewMixin.get_context_data()"""
        return None

    @property
    def outcome(self):
        outcome = []
        if self.appt_date:
            outcome.append('Appt. scheduled')
        elif self.may_call == NO:
            outcome.append('Do not call')
        return outcome

    def log_entries(self):
        return self.__class__.objects.filter(log=self.log)

    class Meta:
        unique_together = ('call_datetime', 'log')
        app_label = 'esr21_follow'
        verbose_name = 'Call Log Entry'
        verbose_name_plural = 'Call Log Entries'

