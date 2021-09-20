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

    @property
    def ideal_date_due(self):
        """Ideal date due to see a participant.
        """
        return self.object.timepoint_datetime

    @property
    def earliest_date_due(self):
        """Returns the earlist date to see a participant.
        """
        visit_definition = self.object.visits.get(self.object.visit_code)

        return self.ideal_date_due - visit_definition.rlower

    @property
    def latest_date_due(self):
        """Returns the last date to see a participant.
        """
        visit_definition = self.object.visits.get(self.object.visit_code)

        return self.ideal_date_due + visit_definition.rupper
