from datetime import timedelta
from dateutil.parser import parse
import datetime
import pandas as pd
import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import (
    ListboardFilterViewMixin, SearchFormViewMixin)
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin
from edc_appointment.models import Appointment
from edc_appointment.constants import IN_PROGRESS_APPT, INCOMPLETE_APPT, COMPLETE_APPT
from edc_appointment.constants import  NEW_APPT

from ..model_wrappers import FollowAppointmentModelWrapper
from ..models import FollowExportFile
from ..forms import AppointmentsWindowForm
from .download_report_mixin import DownloadReportMixin
from .filters import ListboardViewFilters
from .appointment_queryset_view_mixin import AppointmentQuerysetViewMixin
from edc_base.utils import get_utcnow


class AppointmentListboardView(NavbarViewMixin, EdcBaseViewMixin,
                               ListboardFilterViewMixin, SearchFormViewMixin,
                               AppointmentQuerysetViewMixin,
                               DownloadReportMixin, ListboardView, FormView):

    form_class = AppointmentsWindowForm
    listboard_template = 'esr21_follow_appt_listboard_template'
    listboard_url = 'esr21_follow_appt_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"

    model = 'edc_appointment.appointment'
    listboard_view_filters = ListboardViewFilters()
    model_wrapper_cls = FollowAppointmentModelWrapper
    navbar_name = 'esr21_follow'
    navbar_selected_item = 'appointments'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'esr21_follow_appt_listboard_url'

    def get_success_url(self):
        return reverse('esr21_follow:esr21_follow_appt_listboard_url')

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

    def export(self, queryset=None, start_date=None, end_date=None):
        """Export data.
        """
        data = []
        if start_date and end_date:
            queryset = queryset.objects.filter(
                created__date__gte=start_date,
                created__date__lte=end_date)
        for obj in queryset:
            data.append(
                {'subject_identifier': getattr(obj, 'subject_identifier'),
                'visit_code': getattr(obj, 'visit_code'),
                 'appt_datetime': getattr(obj, 'appt_datetime')})
        df = pd.DataFrame(data)
        self.download_data(
            description='Appointment and windows',
            start_date=start_date,
            end_date=end_date,
            report_type='appointments_window_periods',
            df=df)

    def form_valid(self, form):
        start_date = None
        end_date = None
        if form.is_valid():
            start_date = form.data['start_date']
            end_date = form.data['end_date']
        appointment_downloads = FollowExportFile.objects.filter(
            description='Appointment and windows').order_by('uploaded_at')
        context = self.get_context_data(**self.kwargs)
        context.update(
            appointment_downloads=appointment_downloads,)
        return HttpResponseRedirect(
                    reverse('esr21_follow:esr21_follow_appt_listboard_url')+
                    f"?start_date={start_date}&end_date={end_date}")

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        object_list = context.get('object_list')
        if self.request.GET.get('export') == 'yes':
            queryset = context.get('object_list')  # from ListView
            self.export(queryset=queryset)
            msg = (f'File generated successfully.  Go to the download list to download file.')
            messages.add_message(
                self.request, messages.SUCCESS, msg)
        
        if self.request.method == 'POST':
            appt_filter_form = AppointmentsWindowForm(self.request.POST)
            start_date = (appt_filter_form['start_date'].value())
            end_date = (appt_filter_form['end_date'].value())
            
            start_date = parse(start_date).date()
            end_date = parse(end_date).date()
            
            update_request = self.request.POST.copy()
            
            update_request.update({'start_date': start_date})
            update_request.update({'end_date': end_date})
            
            appt_filter_form = AppointmentsWindowForm(update_request)
            if appt_filter_form.is_valid():
                start_date = appt_filter_form.data['start_date']
                end_date = appt_filter_form.data['end_date']
                queryset = self.get_queryset()
                object_list = queryset.filter(
                    appt_datetime__date__gte=start_date,
                    appt_datetime__date__lte=end_date)
                wrapped_queryset = self.get_wrapped_queryset(object_list)
                self.object_list = wrapped_queryset

        appointment_downloads = FollowExportFile.objects.filter(
            description='Appointment and windows').order_by('uploaded_at')
            
            
            
        booked_today = Appointment.objects.filter(appt_datetime__date=get_utcnow().date()).count()
        booked_today_done = Appointment.objects.filter(
            appt_datetime__date=get_utcnow().date(),
            appt_status=COMPLETE_APPT).count()
        booked_today_pending = Appointment.objects.filter(
            appt_datetime__date=get_utcnow().date(),
            appt_status=NEW_APPT).count()
        booked_today_incomplete = Appointment.objects.filter(
            appt_datetime__date=get_utcnow().date(),
            appt_status=INCOMPLETE_APPT).count()
        booked_today_inprogress = Appointment.objects.filter(
            appt_datetime__date=get_utcnow().date(),
            appt_status=IN_PROGRESS_APPT).count()

        booked_tomorrow = Appointment.objects.filter(
            appt_datetime__date=get_utcnow().date() + timedelta(days=1)).count()
        booked_tomorrow_done = Appointment.objects.filter(
            appt_datetime__date=get_utcnow().date() + timedelta(days=1),
            appt_status=COMPLETE_APPT).count()
        booked_tomorrow_pending = Appointment.objects.filter(
            appt_datetime__date=get_utcnow().date() + timedelta(days=1),
            appt_status=NEW_APPT).count()
        booked_tomorrow_incomplete = Appointment.objects.filter(
            appt_datetime__date=get_utcnow().date() + timedelta(days=1),
            appt_status=INCOMPLETE_APPT).count()
        booked_tomorrow_inprogress = Appointment.objects.filter(
            appt_datetime__date=get_utcnow().date() + timedelta(days=1),
            appt_status=IN_PROGRESS_APPT).count()

        date = get_utcnow().date()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(6)

        booked_this_week = Appointment.objects.filter(
            appt_datetime__date__range=[start_week, end_week]).count()
        booked_this_week_done = Appointment.objects.filter(
            appt_datetime__date__range=[start_week, end_week],
            appt_status=COMPLETE_APPT).count()
        booked_this_week_pending = Appointment.objects.filter(
            appt_datetime__date__range=[start_week, end_week],
            appt_status=NEW_APPT).count()
        booked_this_week_incomplete = Appointment.objects.filter(
            appt_datetime__date__range=[start_week, end_week],
            appt_status=INCOMPLETE_APPT).count()
        booked_this_week_inprogress = Appointment.objects.filter(
            appt_datetime__date__range=[start_week, end_week],
            appt_status=IN_PROGRESS_APPT).count()

        context.update(
            appointment_downloads=appointment_downloads,
            booked_today=booked_today,
            booked_today_done=booked_today_done,
            booked_today_pending=booked_today_pending,
            booked_today_incomplete=booked_today_incomplete,
            booked_today_inprogress=booked_today_inprogress,
            booked_tomorrow=booked_tomorrow,
            booked_tomorrow_done=booked_tomorrow_done,
            booked_tomorrow_pending=booked_tomorrow_pending,
            booked_tomorrow_incomplete=booked_tomorrow_incomplete,
            booked_tomorrow_inprogress=booked_tomorrow_inprogress,
            booked_this_week=booked_this_week,
            booked_this_week_done=booked_this_week_done,
            booked_this_week_pending=booked_this_week_pending,
            booked_this_week_incomplete=booked_this_week_incomplete,
            booked_this_week_inprogress=booked_this_week_inprogress)
        return context
