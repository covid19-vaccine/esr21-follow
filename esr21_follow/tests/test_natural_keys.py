from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_sync.tests import SyncTestHelper
from ..models import Call, Log, LogEntry


class TestNaturalKey(TestCase):

    sync_test_helper = SyncTestHelper()

    def test_natural_key_attrs(self):
        self.sync_test_helper.sync_test_natural_key_attr('esr21_follow')

    def test_get_by_natural_key_attr(self):
        self.sync_test_helper.sync_test_get_by_natural_key_attr('esr21_follow')

    def test_sync_test_natural_keys(self):
        call = Call.objects.create(
            subject_identifier='123-45678',
            scheduled=get_utcnow(),
            visit_code='1000',
            label='worklistfollowupmodelcaller')

        log = Log.objects.create(call=call)

        logentry = LogEntry.objects.create(log=log,
                                           call_reason='schedule_appt',
                                           call_datetime=get_utcnow())

        dict_objs = {'calls': [call, ],
                     'logs': [log, ],
                     'logentries': [logentry, ]}

        self.sync_test_helper.sync_test_natural_keys(dict_objs)
