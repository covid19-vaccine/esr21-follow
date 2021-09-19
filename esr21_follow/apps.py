from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'esr21_follow'
    verbose_name = 'ESR21 Follow'
    admin_site_name = 'esr21_follow_admin'
    extra_assignee_choices = ()
    assignable_users_group = 'assignable users'

    # def ready(self):
        # from .models import cal_log_entry_on_post_save
        # from .models import worklist_on_post_save
