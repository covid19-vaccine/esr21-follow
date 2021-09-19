from django.conf import settings

from edc_navbar import NavbarItem, site_navbars, Navbar

esr21_follow = Navbar(name='esr21_follow')

esr21_follow.append_item(
    NavbarItem(
        name='worklist',
        title='Worklist',
        label='Worklist',
        fa_icon='fa-user-plus',
        url_name=settings.DASHBOARD_URL_NAMES[
            'esr21_follow_listboard_url']))

esr21_follow.append_item(
    NavbarItem(name='followups',
               label='ESR21 Follow UPs',
               fa_icon='fa-cogs',
               url_name='esr21_follow:home_url'))

site_navbars.register(esr21_follow)
