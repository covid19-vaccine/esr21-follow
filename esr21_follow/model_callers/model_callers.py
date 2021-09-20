from edc_call_manager.model_caller import ModelCaller, DAILY
from edc_call_manager.decorators import register
from edc_call_manager.models import Call, Log, LogEntry

from esr21_suject.models import PersonalContactInfo

from .models import WorkList


@register(WorkList)
class WorkListFollowUpModelCaller(ModelCaller):
    call_model = Call
    log_model = Log
    log_entry_model = LogEntry
    locator_model = (PersonalContactInfo, 'subject_identifier')
#     consent_model = (SubjectConsent, 'subject_identifier')
    log_entry_model = LogEntry
    log_model = Log
    interval = DAILY
