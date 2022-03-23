from django.test.testcases import TestCase

from edc_base.utils import get_utcnow

from ..models import WorkList, Call


class TestCallManager(TestCase):

    def setUp(self):
        pass

    def test_create_worklist_model(self):
        """Test if a start model created a call instance.
        """
        WorkList.objects.create(appt_datetime=get_utcnow(),
                                subject_identifier='035-123456')
        self.assertEqual(
            Call.objects.filter(subject_identifier='035-123456').count(), 1)
