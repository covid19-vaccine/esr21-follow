from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'esr21_follow'
    verbose_name = 'ESR21 Follow'
    admin_site_name = 'esr21_follow_admin'
    extra_assignee_choices = ()
    assignable_users_group = 'assignable users'

    def ready(self):
        from .models import cal_log_entry_on_post_save
        from .models import appointment_on_post_save


if settings.APP_NAME == 'esr21_follow':

    from datetime import datetime
    from dateutil.tz import gettz

    from edc_appointment.appointment_config import AppointmentConfig
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
    from edc_appointment.constants import COMPLETE_APPT
    from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfigs
    from edc_timepoint.apps import AppConfig as BaseEdcTimepointAppConfig
    from edc_senaite_interface.apps import AppConfig as BaseEdcSenaiteInterfaceAppConfig
    from edc_timepoint.timepoint import Timepoint
    from edc_lab.apps import AppConfig as BaseEdcLabAppConfig
    from edc_timepoint.timepoint_collection import TimepointCollection
    from edc_visit_tracking.apps import (
        AppConfig as BaseEdcVisitTrackingAppConfig)


    class EdcSenaiteInterfaceAppConfig(BaseEdcSenaiteInterfaceAppConfig):
        host = "https://senaite-server.bhp.org.bw/"
        client = "BHP150 | AZD1222"
        sample_type_match = {'humoral_immunogenicity': 'Serum',
                             'sars_cov2_serology': 'Serum',
                             'sars_cov2_pcr': 'Swab',
                             'hematology': 'Whole Blood EDTA',
                             'urine_hcg': 'Urine'}
        container_type_match = {'humoral_immunogenicity': 'Cryogenic vial',
                                'sars_cov2_serology': 'Cryogenic vial',
                                'sars_cov2_pcr': 'Cryogenic Vial',
                                'hematology': 'EDTA Tube',
                                'urine_hcg': 'Urine Cup'}
        template_match = {'humoral_immunogenicity': 'Serum storage',
                          'sars_cov2_serology': 'SARS-COV-2 Serology',
                          'sars_cov2_pcr': 'SARS-COV-2 PCR',
                          'hematology': 'CBC',
                          'urine_hcg': 'Urine HCG'}


    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        configurations = [
            AppointmentConfig(
                model='edc_appointment.appointment',
                related_visit_model='esr21_subject.subjectvisit',
                appt_type='clinic'),]

    class EdcProtocolAppConfig(BaseEdcProtocolAppConfigs):
        protocol = 'BHP150'
        protocol_name = 'ESR21 Follow'
        protocol_number = '150'
        protocol_title = ''
        study_open_datetime = datetime(
            2020, 8, 14, 0, 0, 0, tzinfo=gettz('UTC'))
        study_close_datetime = datetime(
            2025, 8, 13, 23, 59, 59, tzinfo=gettz('UTC'))

    class EdcTimepointAppConfig(BaseEdcTimepointAppConfig):
        timepoints = TimepointCollection(
            timepoints=[
                Timepoint(
                    model='edc_appointment.appointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
                Timepoint(
                    model='edc_appointment.historicalappointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
            ])


    class EdcLabAppConfig(BaseEdcLabAppConfig):
        requisition_model = 'esr21_subject.subjectrequisition'
        result_model = 'edc_lab.result'


    class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
        visit_models = {
            'esr21_subject': (
                'subject_visit', 'esr21_subject.subjectvisit'),
}