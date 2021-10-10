from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from edc_base.sites import SiteModelFormMixin

from .models import Booking, WorkList, LogEntry


class WorkListForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = WorkList
        fields = '__all__'

class BookingForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = Booking
        fields = '__all__'


class AppointmentsWindowForm(forms.Form):

    start_date = forms.DateField(
        required=True, label='Start date',
        widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(
        required=True, label='End date',
        widget=forms.TextInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_id = 'appointment'
        self.helper.form_action = 'esr21_follow:esr21_follow_appt_listboard_url'
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            'start_date',
            'end_date',
            Submit('submit', u'filter report', css_class="btn btn-sm btn-default")
        )


class AppointmentRegistrationForm(forms.Form):

    first_name = forms.CharField(
            required=True, label='Firstname')

    middle_name = forms.CharField(
            required=False, label='Middlename')

    last_name = forms.CharField(
            required=True, label='Lastname')

    subject_cell = forms.IntegerField(
        required=True, label='Cell Number')

    booking_date = forms.DateField(
        required=True, label='Booking date',
        widget=forms.TextInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_id = 'appointment_registration'
        self.helper.form_action = 'esr21_follow:esr21_follow_book_listboard_url'
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            'first_name',
            'middle_name',
            'last_name',
            'subject_cell',
            'booking_date',
            Submit('submit', u'Book participant', css_class="btn btn-sm btn-default")
        )

class LogEntryForm(
        SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = LogEntry
        fields = '__all__'
