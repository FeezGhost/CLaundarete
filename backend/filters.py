# from django.http import request
from django.forms.widgets import DateInput
import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter, ChoiceFilter, DateFromToRangeFilter
from django_filters.filters import MultipleChoiceFilter
from .models import *
from tempus_dominus.widgets import DateTimePicker, DatePicker
from django_filters.widgets import RangeWidget

class OrderFilter(django_filters.FilterSet):
    start_date = DateFromToRangeFilter(field_name="date_started", widget=RangeWidget(attrs={'type': 'date'}), label='Date_Started')
    end_date = DateFromToRangeFilter(field_name="date_end", widget=RangeWidget(attrs={'type': 'date'}), label='Date_Ended')
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

def get_launderrette(request):
    launderer = request.user.launderer
    print('launderer')
    launderette = launderer.launderette_set.all()[0]

    return launderette.services_set.all()


class OrderFilter2(django_filters.FilterSet):
    start_date = DateFromToRangeFilter(field_name="date_started", widget=RangeWidget(attrs={'type': 'date'}), label='Date_Started')
    end_date = DateFromToRangeFilter(field_name="date_end", widget=RangeWidget(attrs={'type': 'date'}), label='Date_Ended')
    start_price = NumberFilter(field_name="price", lookup_expr='gte')
    end_price = NumberFilter(field_name="price", lookup_expr='lte')
    start_amount = NumberFilter(field_name="amount", lookup_expr='gte')
    end_amount = NumberFilter(field_name="amount", lookup_expr='lte')
    client_name = CharFilter(field_name='client__name', lookup_expr='icontains')
    status = ChoiceFilter(choices=FILTER_CHOICES, )
    
    class Meta:
        model = Order
        exclude = '__all__'
        fields = ['start_date', 'end_date', 'start_price','start_amount','end_amount', 'client_name','status',
        'services'
        ]

class ReviewFilter(django_filters.FilterSet):
    start_date = DateFromToRangeFilter(field_name="date", widget=RangeWidget(attrs={'type': 'date'}), label='Date_Started')
    start_rating = NumberFilter(field_name="rating", lookup_expr='gte')
    end_rating = NumberFilter(field_name="rating", lookup_expr='lte')
    client_name = CharFilter(field_name='client__name', lookup_expr='icontains')
    launderette_name = CharFilter(field_name='launderette__name', lookup_expr='icontains')
    class Meta:
        model = Review
        exclude = '__all__'
        fields = ['start_date', 'start_rating', 'end_rating', 'client_name']

class ComplaintFilter(django_filters.FilterSet):
    start_date = DateFromToRangeFilter(field_name="date", widget=RangeWidget(attrs={'type': 'date'}), label='Date_Started')
    subject = CharFilter(field_name='subject', lookup_expr='icontains')
    class Meta:
        model = Complaint
        fields = '__all__'

class LaundererFilter(django_filters.FilterSet):
    start_date = DateFromToRangeFilter(field_name="date_joined", widget=RangeWidget(attrs={'type': 'date'}), label='Date_Started')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    city = CharFilter(field_name='city', lookup_expr='icontains')

    class Meta:
        model = Launderer
        fields = '__all__'
        exclude = ["profile_pic"]

class ClientFilter(django_filters.FilterSet):
    start_date = DateFromToRangeFilter(field_name="date_joined", widget=RangeWidget(attrs={'type': 'date'}), label='Date_Started')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Client
        fields = '__all__'
        exclude = ["profile_pic"]

class LaunderetteFilter(django_filters.FilterSet):
    start_date = DateFromToRangeFilter(field_name="date_joined", widget=RangeWidget(attrs={'type': 'date'}), label='Date_Started')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    location = CharFilter(field_name='location', lookup_expr='icontains')
    available_time = CharFilter(field_name='available_time', lookup_expr='icontains')

    class Meta:
        model = Launderette
        fields = '__all__'
        exclude = ["cover_photo"]

