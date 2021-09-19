from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):
    site_title = 'ESR21 Follow'
    site_header = 'ESR21 Follow'
    index_title = 'ESR21 Follow'
    site_url = '/administration/'
    enable_nav_sidebar = False

esr21_follow_admin = AdminSite(name='esr21_follow_admin')
