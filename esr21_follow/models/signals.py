from django.db.models.signals import post_save
from django.dispatch import receiver

from edc_appointment.models import Appointment

from ..models import LogEntry


@receiver(post_save, weak=False, sender=LogEntry,
          dispatch_uid="cal_log_entry_on_post_save")
def cal_log_entry_on_post_save(sender, instance, using, raw, **kwargs):
    if not raw:
        # Update worklist
        from ..models import WorkList
        try:
            work_list = WorkList.objects.get(
                subject_identifier=instance.log.call.subject_identifier,
                visit_code=instance.log.call.visit_code)
        except WorkList.DoesNotExist:
            pass
        else:
            if instance.appt:
                work_list.is_called = True
                work_list.called_datetime = instance.call_datetime
                work_list.user_modified=instance.user_modified
                work_list.save()



@receiver(post_save, weak=False, sender=Appointment,
          dispatch_uid="appointment_on_post_save")
def appointment_on_post_save(sender, instance, using, raw, **kwargs):
    if not raw:
        # Update or Create worklist
        from ..models import WorkList
        try:
            work_list = WorkList.objects.get(
                subject_identifier=instance.subject_identifier,
                visit_code=instance.visit_code)
        except WorkList.DoesNotExist:
            WorkList.objects.create(
                subject_identifier=instance.subject_identifier,
                appt_status=instance.appt_status,
                user_created=instance.user_created,
                visit_code=instance.visit_code,
                appt_datetime=instance.appt_datetime)
        else:
            work_list.appt_status = instance.appt_status
            work_list.appt_datetime = instance.appt_datetime
            work_list.save()
