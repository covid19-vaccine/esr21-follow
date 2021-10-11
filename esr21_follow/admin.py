from django.contrib import admin

from django_revision.modeladmin_mixin import ModelAdminRevisionMixin

from edc_base.sites.admin import ModelAdminSiteMixin
from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin)
from edc_model_admin import audit_fieldset_tuple
from edc_model_admin import ModelAdminBasicMixin
from edc_model_admin.changelist_buttons import ModelAdminChangelistModelButtonMixin
from edc_call_manager.admin import ModelAdminLogEntryMixin

from .admin_site import esr21_follow_admin
from .forms import BookingForm, WorkListForm

from .models import Booking, Call, WorkList, Log, LogEntry


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin,
                      ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin,
                      ModelAdminRedirectOnDeleteMixin,
                      ModelAdminSiteMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


@admin.register(WorkList, site=esr21_follow_admin)
class WorkListAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = WorkListForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'report_datetime',
                'prev_study',
                'is_called',
                'called_datetime',
                'visited',)}),
        audit_fieldset_tuple)

    instructions = ['Complete this form once per day.']

    list_display = ('subject_identifier', 'is_called')


@admin.register(Booking, site=esr21_follow_admin)
class BookingAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = BookingForm

    fieldsets = (
        (None, {
            'fields': (
                'first_name',
                'middle_name',
                'last_name',
                'subject_cell',
                'booking_date',)}),
        audit_fieldset_tuple)

    list_display = ('first_name', 'last_name', 'subject_cell',)


class ModelAdminCallMixin(ModelAdminChangelistModelButtonMixin, ModelAdminBasicMixin):

    date_hierarchy = 'modified'

    mixin_fields = (
        'call_attempts',
        'call_status',
        'call_outcome',
    )

    mixin_radio_fields = {'call_status': admin.VERTICAL}

    list_display_pos = None
    mixin_list_display = (
        'subject_identifier',
        'call_attempts',
        'call_outcome',
        'scheduled',
        'label',
        'first_name',
        'initials',
        'user_created',
    )

    mixin_list_filter = (
        'call_status',
        'call_attempts',
        'modified',
        'hostname_created',
        'user_created',
    )

    mixin_readonly_fields = (
        'call_attempts',
    )

    mixin_search_fields = ('subject_identifier', 'initials', 'label')


@admin.register(Call, site=esr21_follow_admin)
class CallAdmin(ModelAdminMixin, ModelAdminCallMixin, admin.ModelAdmin):
    pass


@admin.register(Log, site=esr21_follow_admin)
class LogAdmin(ModelAdminMixin, admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(LogEntry, site=esr21_follow_admin)
class LogEntryAdmin(ModelAdminMixin, admin.ModelAdmin):

    fields = (
        'log',
        'subject_identifier',
        'call_reason',
        'call_datetime',
        'contact_type',
        'appt_date',
        'appt_location',
        'appt_location_other',
        'call_status',
        'reason_unsuccesful'
    )

    radio_fields = {'call_reason': admin.VERTICAL,
                    'contact_type': admin.VERTICAL,
                    'appt_location': admin.VERTICAL,
                    'call_status': admin.VERTICAL,
                    'reason_unsuccesful': admin.VERTICAL}

    list_display = ('log', 'call_datetime', 'appt_date', )

    search_fields = ('id', 'log__call__subject_identifier')

    list_filter = (
        'call_datetime',
        'appt_date',
        'created',
        'modified',
        'hostname_created',
        'hostname_modified',
    )

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['log'].queryset = \
            Log.objects.filter(id=request.GET.get('log'))
        return super().render_change_form(request, context, *args, **kwargs)
