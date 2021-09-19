from django import forms
from edc_form_validators import FormValidatorMixin


from edc_base.sites import SiteModelFormMixin

from .models import WorkList, LogEntry
from .form_validations import LogEntryFormValidator


class WorkListForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = WorkList
        fields = '__all__'


class LogEntryForm(
        SiteModelFormMixin, FormValidatorMixin,
        forms.ModelForm):

    form_validator_cls = LogEntryFormValidator

    study_maternal_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    phone_num_type = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label='Which phone number(s) was used for contact?')

    phone_num_success = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label='Which number(s) were you successful in reaching?')

    class Meta:
        model = LogEntry
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = self.custom_choices
        self.fields['phone_num_type'].choices = choices
        self.fields['phone_num_success'].choices = choices + (('none_of_the_above', 'None of the above'),)
