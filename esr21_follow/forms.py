from django import forms
from edc_form_validators import FormValidatorMixin


from edc_base.sites import SiteModelFormMixin

from .models import WorkList


class WorkListForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = WorkList
        fields = '__all__'
