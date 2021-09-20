from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from .models import WorkList


class WorkListForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = WorkList
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