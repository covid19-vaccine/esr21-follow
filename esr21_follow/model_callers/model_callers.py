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
