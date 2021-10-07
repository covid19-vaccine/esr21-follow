from django.db.models.signals import post_save
from django.dispatch import receiver

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
