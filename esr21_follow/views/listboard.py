import re

# from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls.base import reverse
from django.utils.decorators import method_decorator

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import (
    ListboardFilterViewMixin, SearchFormViewMixin)
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin
from edc_base.utils import get_utcnow
from edc_appointment.models import Appointment

from ..model_wrappers import WorkListModelWrapper
from ..models import WorkList
from .filters import ListboardViewFilters
from .worklist_queryset_view_mixin import WorkListQuerysetViewMixin
from django.core.exceptions import ValidationError


class ListboardView(NavbarViewMixin, EdcBaseViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin,
                    WorkListQuerysetViewMixin,
                    ListboardView):

    listboard_template = 'esr21_follow_listboard_template'
    listboard_url = 'esr21_follow_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"

    model = 'esr21_follow.worklist'
    listboard_view_filters = ListboardViewFilters()
    model_wrapper_cls = WorkListModelWrapper
    navbar_name = 'esr21_follow'
    navbar_selected_item = 'worklist'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'esr21_follow_listboard_url'

    def get_success_url(self):
        return reverse('esr21_follow:esr21_follow_listboard_url')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        identifiers = self.request.GET.get('identifiers', None)
        if identifiers:
            identifiers = identifiers.split(',')
            self.create_worklist(identifiers=identifiers)

        context.update(
            total_results=self.get_queryset().count(),
            called_subject=WorkList.objects.filter(is_called=True).count(),
            visited_subjects=WorkList.objects.filter(visited=True).count(),
        )
        return context

    def create_worklist(self, identifiers=None):
        """Create a worklist.
        """
        for identifier in identifiers:
            subject_identifier, visit_code = identifier.split('|')
            try:
                appointment = Appointment.objects.get(
                    subject_identifier=subject_identifier, visit_code=visit_code)
            except Appointment.DoesNotExist:
                raise ValidationError(
                    f'Missing appointment for visit {visit_code}, {subject_identifier}')
            else:
                try:
                    WorkList.objects.get(
                        subject_identifier=identifier, visit_code=visit_code)
                except WorkList.DoesNotExist:
                    WorkList.objects.create(
                        subject_identifier=subject_identifier,
                        appointment_id=appointment.id,
                        user_created=self.request.user.username,
                        assigned=self.request.user.username,
                        date_assigned=get_utcnow().date(),
                        visit_code=visit_code,
                        appt_datetime=appointment.appt_datetime)
