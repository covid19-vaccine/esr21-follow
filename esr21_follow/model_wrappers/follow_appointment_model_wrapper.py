from django.conf import settings
from edc_model_wrapper import ModelWrapper
from esr21_subject.models import InformedConsent
from .consent_model_wrapper_mixin import ConsentModelWrapperMixin


class FollowAppointmentModelWrapper(ConsentModelWrapperMixin, ModelWrapper):

    model = 'edc_appointment.appointment'
    querystring_attrs = ['subject_identifier']
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'esr21_follow_appt_listboard_url')

    @property
    def subject_consent(self):
        """Returns a subject consent object.
        """
        return InformedConsent.objects.filter(
            subject_identifier=self.object.subject_identifier).last()

    @property
    def gender(self):
        """Returns the gender of the participant.
        """
        return self.subject_consent.gender
