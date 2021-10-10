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
    NavbarItem(
        name='appointments',
        title='appointments',
        label='appointments',
        fa_icon='fa-user-plus',
        url_name=settings.DASHBOARD_URL_NAMES[
            'esr21_follow_appt_listboard_url']))

esr21_follow.append_item(
    NavbarItem(
        name='book',
        title='book',
        label='Screening Bookings',
        fa_icon='fa-user-plus',
        url_name=settings.DASHBOARD_URL_NAMES[
            'esr21_follow_book_listboard_url']))

site_navbars.register(esr21_follow)
