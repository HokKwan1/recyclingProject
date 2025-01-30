import django_filters
from homepage.models import Request

class RequestFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Request.STATUS_CHOICES)
    date_created = django_filters.DateFromToRangeFilter()
    city = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Request
        fields = ["status", "date_created", "city"]