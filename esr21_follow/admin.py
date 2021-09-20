from django.apps import apps as django_apps
from django.contrib import admin

from django_revision.modeladmin_mixin import ModelAdminRevisionMixin


from edc_model_admin.model_admin_next_url_redirect_mixin import ModelAdminNextUrlRedirectError
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin)
from edc_model_admin import audit_fieldset_tuple
from edc_model_admin import ModelAdminBasicMixin
from edc_model_admin.changelist_buttons import ModelAdminChangelistModelButtonMixin

from .admin_site import esr21_follow_admin
from .forms import WorkListForm
from .models import WorkList


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
