from edc_call_manager.model_caller import ModelCaller, DAILY
from edc_call_manager.decorators import register

from esr21_subject.models import PersonalContactInfo

from ..models import Call, Log, LogEntry, WorkList


@register(WorkList)
class WorkListFollowUpModelCaller(ModelCaller):
    call_model = Call
    log_model = Log
    log_entry_model = LogEntry
    locator_model = (PersonalContactInfo, 'subject_identifier')
    # consent_model = (InformedConsent, 'subject_identifier')
    log_entry_model = LogEntry
    log_model = Log
    interval = DAILY

    def personal_details_from_subject(self, instance):
        """Returns additional options from the subject model to be used to create a Call instance.

        Used if the consent is not available."""
        subject = self.subject(instance.subject_identifier)
        if subject:
            options = {'subject_identifier': subject.subject_identifier,
                       'first_name': subject.first_name,
                       'initials': subject.initials,
                       'visit_code': instance.visit_code}
        else:
            options = {
                'subject_identifier': instance.subject_identifier,
                'visit_code': instance.visit_code}
        return options