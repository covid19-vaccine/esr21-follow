from django.conf import settings
from edc_model_wrapper import ModelWrapper


class LogEntryModelWrapper(ModelWrapper):

    model = 'edc_call_manager.logentry'
    querystring_attrs = ['log', 'subject_identifier']
    next_url_attrs = ['log', 'subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get('esr21_follow_listboard_url')

    @property
    def log(self):
        return self.object.log
