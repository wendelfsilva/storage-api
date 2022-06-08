from django_filters import filterset

from core import models

LIKE = 'icontains'
EQUALS = 'exact'
LTE = 'lte'
GTE = 'gte'


# Filters define the filter behavior for each view.

class DocumentFilter(filterset.FilterSet):
    id = filterset.NumberFilter(lookup_expr=EQUALS)
    path = filterset.CharFilter(lookup_expr=LIKE)
    start_date = filterset.DateFilter(field_name='uploaded_at__date', lookup_expr=GTE)
    end_date = filterset.DateFilter(field_name='uploaded_at__date', lookup_expr=LTE)

    class Meta:
        model = models.Document
        fields = [
            'id',
            'path',
            'start_date',
            'end_date',
        ]
