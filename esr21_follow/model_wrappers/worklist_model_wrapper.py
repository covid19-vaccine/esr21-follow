from django.apps import apps as django_apps
from django.conf import settings

from edc_model_wrapper import ModelWrapper

from ..models import Call, Log, LogEntry
from .log_entry_model_wrapper import LogEntryModelWrapper


class WorkListModelWrapper(ModelWrapper):

    model = 'esr21_follow.worklist'
    querystring_attrs = ['subject_identifier']
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'esr21_follow_listboard_url')

    @property
    def subject_locator(self):
        SubjectLocator = django_apps.get_model(
            'esr21_subject.PersonalContactInfo')
        if self.object.subject_identifier:
            try:
                locator = SubjectLocator.objects.get(
                    subject_identifier=self.object.subject_identifier)
            except SubjectLocator.DoesNotExist:
                pass
            else:
                return locator
        return None

    @property
    def call_datetime(self):
        return self.object.called_datetime

    @property
    def call(self):
        call = Call.objects.filter(
            subject_identifier=self.object.subject_identifier,
            visit_code=self.object.visit_code).order_by('scheduled').last()
        return str(call.id)

    @property
    def call_log(self):
        call = Call.objects.filter(
            subject_identifier=self.object.subject_identifier,
            visit_code=self.object.visit_code).order_by('scheduled').last()
        call_log = Log.objects.get(call=call)
        return str(call_log.id)

    @property
    def log_entries(self):
        wrapped_entries = []
        call = Call.objects.filter(
            subject_identifier=self.object.subject_identifier,
            visit_code=self.object.visit_code).order_by('scheduled').last()
        log_entries = LogEntry.objects.filter(
            log__call__subject_identifier=call.subject_identifier).order_by('-call_datetime')[:3]
        for log_entry in log_entries:
            wrapped_entries.append(
                LogEntryModelWrapper(log_entry))
        return wrapped_entries

    @property
    def locator_phone_numbers(self):
        """Return all contact numbers on the locator.
        """
        field_attrs = [
            'subject_cell',
            'subject_cell_alt',
            'subject_phone',
            'subject_phone_alt',
            'subject_work_phone',
            'indirect_contact_cell',
            'indirect_contact_phone', ]
        if self.subject_locator:
            phone_choices = ()
            for field_attr in field_attrs:
                value = getattr(self.subject_locator, field_attr)
                if value:
                    phone_choices += ((field_attr, value),)
            return phone_choices

    @property
    def call_log_required(self):
        """Return True if the call log is required.
        """
        if self.locator_phone_numbers:
            return True
        return False

    @property
    def log_entry(self):
        log = Log.objects.get(id=self.call_log)

        logentry = LogEntry(log=log)
        return LogEntryModelWrapper(logentry)

    @property
    def subject_consent(self):
        return django_apps.get_model(
            'esr21_subject.informedconsent').objects.filter(
            subject_identifier=self.object.subject_identifier).last()

    @property
    def may_visit_home(self):
        if self.subject_locator:
            return self.subject_locator.may_visit_home
        return None

    @property
    def first_name(self):
        return self.subject_consent.first_name

    @property
    def last_name(self):
        return self.subject_consent.last_name

    @property
    def contacts(self):
        if self.subject_locator:
            return ', '.join([
                self.subject_locator.subject_cell or '',
                self.subject_locator.subject_cell_alt or '',
                self.subject_locator.subject_phone or '',
                self.subject_locator.subject_phone_alt or ''])
        return None

    @property
    def survey_schedule(self):
        return None

