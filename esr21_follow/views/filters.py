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
