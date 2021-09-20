from django.urls import path
from django.views.generic.base import RedirectView
from edc_dashboard import UrlConfig
from .admin_site import esr21_follow_admin
from .views import AppointmentListboardView, ListboardView, HomeView

app_name = 'esr21_follow'

subject_identifier = '150\-[0-9\-]+'

urlpatterns = [
    path('admin/', esr21_follow_admin.urls),
    path('home', HomeView.as_view(), name='home_url'),
    path('', RedirectView.as_view(url='admin/'), name='admin_url'),
]

esr21_follow_listboard_url_config = UrlConfig(
    url_name='esr21_follow_listboard_url',
    view_class=ListboardView,
    label='esr21_follow_listboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)


esr21_follow_appt_listboard_url_config = UrlConfig(
    url_name='esr21_follow_appt_listboard_url',
    view_class=AppointmentListboardView,
    label='esr21_follow_appt_listboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)


urlpatterns += esr21_follow_listboard_url_config.listboard_urls
urlpatterns += esr21_follow_appt_listboard_url_config.listboard_urls
