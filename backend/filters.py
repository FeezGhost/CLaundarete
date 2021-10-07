import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter, ChoiceFilter
from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_started", lookup_expr='gte')
    end_date = DateFilter(field_name="date_end", lookup_expr='lte')
    start_price = NumberFilter(field_name="price", lookup_expr='gte')
    end_price = NumberFilter(field_name="price", lookup_expr='lte')
    start_amount = NumberFilter(field_name="amount", lookup_expr='gte')
    end_amount = NumberFilter(field_name="amount", lookup_expr='lte')
    client_name = CharFilter(field_name='client__name', lookup_expr='icontains')
    class Meta:
        model = Order
        exclude = '__all__'
        fields = ['start_date', 'end_date', 'start_price','start_amount','end_amount', 'client_name']

FILTER_CHOICES = (
    ('finished', 'Finished'),
    ('declined', 'Declined'),
)

class OrderFilter2(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_started", lookup_expr='gte')
    end_date = DateFilter(field_name="date_end", lookup_expr='lte')
    start_price = NumberFilter(field_name="price", lookup_expr='gte')
    end_price = NumberFilter(field_name="price", lookup_expr='lte')
    start_amount = NumberFilter(field_name="amount", lookup_expr='gte')
    end_amount = NumberFilter(field_name="amount", lookup_expr='lte')
    client_name = CharFilter(field_name='client__name', lookup_expr='icontains')
    status = ChoiceFilter(choices=FILTER_CHOICES)
    class Meta:
        model = Order
        exclude = '__all__'
        fields = ['start_date', 'end_date', 'start_price','start_amount','end_amount', 'client_name','status']

class ReviewFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date", lookup_expr='gte')
    end_date = DateFilter(field_name="date", lookup_expr='lte')
    start_rating = NumberFilter(field_name="rating", lookup_expr='gte')
    end_rating = NumberFilter(field_name="rating", lookup_expr='lte')
    client_name = CharFilter(field_name='client__name', lookup_expr='icontains')
    class Meta:
        model = Order
        exclude = '__all__'
        fields = ['start_date', 'end_date', 'start_rating', 'end_rating', 'client_name']

class ComplaintFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date", lookup_expr='gte')
    end_date = DateFilter(field_name="date", lookup_expr='lte')
    subject = CharFilter(field_name='subject', lookup_expr='icontains')
    class Meta:
        model = Order
        fields = '__all__'

class LaundererFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_joined", lookup_expr='gte')
    end_date = DateFilter(field_name="date_joined", lookup_expr='lte')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Launderer
        fields = '__all__'
        exclude = ["profile_pic"]

class ClientFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_joined", lookup_expr='gte')
    end_date = DateFilter(field_name="date_joined", lookup_expr='lte')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Client
        fields = '__all__'
        exclude = ["profile_pic"]

class LaunderetteFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_joined", lookup_expr='gte')
    end_date = DateFilter(field_name="date_joined", lookup_expr='lte')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    location = CharFilter(field_name='location', lookup_expr='icontains')
    available_time = CharFilter(field_name='available_time', lookup_expr='icontains')

    class Meta:
        model = Launderette
        fields = '__all__'
        exclude = ["cover_photo"]

