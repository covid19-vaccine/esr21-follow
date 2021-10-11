from edc_form_validators import FormValidator


class LogEntryFormValidator(FormValidator):

    def clean(self):
        self.required_if(
            'unsuccessful',
            field='call_status',
            field_required='reason_unsuccesful')
