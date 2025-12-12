from netbox.filtersets import ChangeLoggedModelFilterSet, OrganizationalModelFilterSet, NetBoxModelFilterSet
from tenancy.filtersets import ContactModelFilterSet, TenancyFilterSet
import django_filters
from .choices import PhoneNumberStatusChoises, PhoneRangeTypeChoices, PhoneCountryCodeChoises
from .models import PhoneNumber, PhoneNumberRange, Sim, SimAdmin
from django.utils.translation import gettext as _
from circuits.models import Provider, ProviderAccount
from utilities.filters import MultiValueCharFilter, MultiValueNumberFilter
from django.db.models import Q

class PhoneNumberRangeFilterSet(NetBoxModelFilterSet, TenancyFilterSet):
    status = django_filters.MultipleChoiceFilter(
        choices=PhoneNumberStatusChoises,
        null_value=None
    )

    country_code = django_filters.MultipleChoiceFilter(
        choices=PhoneCountryCodeChoises,
        null_value=None
    )

    type = django_filters.MultipleChoiceFilter(
        choices=PhoneRangeTypeChoices,
        null_value=None
    )    

    class Meta:
        model = PhoneNumberRange
        fields = ('id', 'status', 'description', 'country_code', 'start_number', 'end_number', 'type',)


class PhoneNumberFilterSet(NetBoxModelFilterSet, TenancyFilterSet):
    status = django_filters.MultipleChoiceFilter(
        choices=PhoneNumberStatusChoises,
        null_value=None
    )

    country_code = django_filters.MultipleChoiceFilter(
        choices=PhoneCountryCodeChoises,
        null_value=None
    )

    type = django_filters.MultipleChoiceFilter(
        choices=PhoneRangeTypeChoices,
        null_value=None
    )  

    class Meta:
        model = PhoneNumber
        fields = ('id', 'status', 'description', 'number', 'country_code', 'incoming_dialpeer', 'outgoining_dialpeer', 'region', 'primary_voice_circuit', 'primary_virtual_circuit', 'secondary_voice_circuit', 'secondary_virtual_circuit', 'type')


class SimFilterSet(NetBoxModelFilterSet, TenancyFilterSet):

    provider_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Provider.objects.all(),
        label=_('Provider (ID)'),
    )
    provider = django_filters.ModelMultipleChoiceFilter(
        field_name='provider__slug',
        queryset=Provider.objects.all(),
        to_field_name='slug',
        label=_('Provider (slug)'),
    )
    provider_account_id = django_filters.ModelMultipleChoiceFilter(
        field_name='provider_account',
        queryset=ProviderAccount.objects.all(),
        label=_('Provider account (ID)'),
    )
    provider_account = django_filters.ModelMultipleChoiceFilter(
        field_name='provider_account__account',
        queryset=Provider.objects.all(),
        to_field_name='account',
        label=_('Provider account (account)'),
    )


    class Meta:
        model = Sim
        fields = ('id',  'description', 'sim_id', 'iccid', 'msisdn')

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
                Q(value__icontains=value)
                | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)

class SimAdminFilterSet(NetBoxModelFilterSet):

    class Meta:
        model = SimAdmin
        fields = ('id', )