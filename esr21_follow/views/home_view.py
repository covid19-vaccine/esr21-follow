from dateutil.parser import parse

from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.views.generic.edit import FormView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from ..forms import AppointmentRegistrationForm
from ..models import Booking
from ..model_wrappers import BookingModelWrapper


class HomeView(
        EdcBaseViewMixin, NavbarViewMixin,
        ListView, FormView):

    form_class = AppointmentRegistrationForm
    paginate_by = 2
    model = Booking
    template_name = 'esr21_follow/home.html'
    navbar_name = 'esr21_follow'
    navbar_selected_item = 'followups'

    def get_success_url(self):
        return reverse('esr21_follow:home_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Bookings
        if self.request.method == 'POST':
            booking_form = AppointmentRegistrationForm(self.request.POST)
            booking_date = (booking_form['booking_date'].value())
            booking_date = parse(booking_date).date()
            update_request = self.request.POST.copy()
            update_request.update({'booking_date': booking_date})
            booking_form = AppointmentRegistrationForm(update_request)
            if booking_form.is_valid():
                first_name = booking_form.data['first_name']
                middle_name = booking_form.data['middle_name']
                last_name = booking_form.data['last_name']
                subject_cell = booking_form.data['subject_cell']
                booking_date = booking_form.data['booking_date']

                options = {
                    'first_name': first_name,
                    'middle_name': middle_name,
                    'last_name': last_name,
                    'subject_cell': subject_cell,
                    'booking_date': booking_date}
                try:
                    Booking.objects.get(subject_cell=subject_cell)
                except Booking.DoesNotExist:
                    Booking.objects.create(**options)

        bookings = Booking.objects.all()
        bookings = [BookingModelWrapper(obj) for obj in bookings]
        paginator = Paginator(bookings, 6) # Show 6 contacts per page.
        object_list = self.get_queryset()
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context.update(
            bookings=bookings,
            page_obj=page_obj)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
