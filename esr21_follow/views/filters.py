from datetime import timedelta

from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters
from edc_base.utils import get_utcnow


class ListboardViewFilters(ListboardViewFilters):

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    today = ListboardFilter(
        label='Today',
        position=10,
        lookup={'appt_datetime__date': get_utcnow().date()})

    tomorrow = ListboardFilter(
        label='Tomorrow',
        position=10,
        lookup={'appt_datetime__date': get_utcnow().date() + timedelta(days=1)})


class ScreeningListboardViewFilters(ListboardViewFilters):

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    today = ListboardFilter(
        label='Today',
        position=6,
        lookup={'booking_date': get_utcnow().date()})

    tomorrow = ListboardFilter(
        label='Tomorrow',
        position=6,
        lookup={'booking_date': get_utcnow().date() + timedelta(days=1)})

    pending = ListboardFilter(
        label='Pending',
        position=6,
        lookup={'appt_status': 'pending'})


    done = ListboardFilter(
        label='Done',
        position=6,
        lookup={'appt_status': 'done'})

    cancelled = ListboardFilter(
        label='Cancelled',
        position=6,
        lookup={'appt_status': 'cancelled'})
