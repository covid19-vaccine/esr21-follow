from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from ..forms import AppointmentRegistrationForm
from ..models import Booking


class HomeView(
        EdcBaseViewMixin, NavbarViewMixin,
        TemplateView, FormView):

    form_class = AppointmentRegistrationForm
    template_name = 'esr21_follow/home.html'
    navbar_name = 'esr21_follow'
    navbar_selected_item = 'followups'

    def get_success_url(self):
        return reverse('esr21_follow:home_url')

    def form_valid(self, form):
        if form.is_valid():
            first_name = form.data['first_name']
            middle_name = form.data['middle_name']
            last_name = form.data['last_name']
            cell_number = form.data['cell_number']
            booking_date = form.data['booking_date']
            options = {
                'first_name': first_name,
                'middle_name': middle_name,
                'last_name': last_name,
                'cell_number': cell_number,
                'booking_date': booking_date}
            try:
                Booking.objects.get()
            except Booking.DoesNotExist:
                Booking.objects.create(**options)
        context = self.get_context_data(**self.kwargs)
        context.update()
        return HttpResponseRedirect(
                    reverse('esr21_follow:home_url'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
