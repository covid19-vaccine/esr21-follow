from django.db.models.constants import LOOKUP_SEP


class AppointmentQuerysetViewMixin:

    appointment_queryset_lookups = []

    @property
    def appointment_lookup_prefix(self):
        appointment_lookup_prefix = LOOKUP_SEP.join(self.appointment_queryset_lookups)
        return f'{appointment_lookup_prefix}__' if appointment_lookup_prefix else ''

    def add_appt_status_filter_options(self, options=None, **kwargs):
        options.update(
            {f'{self.appointment_lookup_prefix}appt_status': 'new',
             f'{self.appointment_lookup_prefix}assigned__isnull': True})
        return options
    

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        options = self.add_appt_status_filter_options(
            options=options, **kwargs)
        return options
