from django.apps import apps as django_apps

from edc_base.model_mixins import ListModelMixin
from edc_sync.site_sync_models import site_sync_models
from edc_sync.sync_model import SyncModel

sync_models = []
app = django_apps.get_app_config('esr21_follow')
for model in app.get_models():
    if (not issubclass(model, ListModelMixin) and
            model._meta.label_lower not in ['esr21_follow.followexportfile']):
        sync_models.append(model._meta.label_lower)

site_sync_models.register(sync_models, SyncModel)
