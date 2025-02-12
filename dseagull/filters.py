import datetime

from django.utils import timezone
from django_filters.rest_framework import FilterSet


class BaseFilterSet(FilterSet):

    def filter_datetime(self, queryset, name, value):  # noqa
        if ',' in value:
            start_at = timezone.make_aware(datetime.datetime.fromtimestamp(int(value.split(',')[0])))
            end_at = timezone.make_aware(datetime.datetime.fromtimestamp(int(value.split(',')[1])))
            query = {
                f'{name}__gte': start_at,
                f'{name}__lte': end_at,
            }
            queryset = queryset.filter(**query)
        return queryset
