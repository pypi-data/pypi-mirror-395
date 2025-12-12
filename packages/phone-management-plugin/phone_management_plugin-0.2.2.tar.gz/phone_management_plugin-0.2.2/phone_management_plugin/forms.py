from django.utils.translation import gettext_lazy as _
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelImportForm, NetBoxModelBulkEditForm
from tenancy.forms import ContactModelFilterForm, TenancyFilterForm
from .models import PhoneNumber, PhoneNumberRange, Sim, SimAdmin
from .choices import PhoneCountryCodeChoises, PhoneRangeTypeChoices, PhoneNumberStatusChoises
from utilities.forms.fields import (
    TagFilterField,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    CSVModelChoiceField,
    CSVChoiceField,
)
from utilities.forms.rendering import FieldSet, TabbedGroups
from netbox.forms import NetBoxModelForm
from tenancy.forms import TenancyForm
from django import forms
from dcim.models import Device, Region
from circuits.models import Circuit, VirtualCircuit
from virtualization.models import VirtualMachine
from tenancy.models import Tenant
from circuits.models import Provider, ProviderAccount


class PhoneNumberRangeForm(TenancyForm, NetBoxModelForm):

    primary_voice_circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all(),
        required=False,
        selector=True,
        label=_("Primary Circuit"),
    )

    primary_virtual_circuit = DynamicModelChoiceField(
        queryset=VirtualCircuit.objects.all(),
        required=False,
        selector=True,
        label=_("Primary Virtual Circuit"),
    )

    secondary_voice_circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all(),
        required=False,
        selector=True,
        label=_("Secondary Circuit"),
    )

    secondary_virtual_circuit = DynamicModelChoiceField(
        queryset=VirtualCircuit.objects.all(),
        required=False,
        selector=True,
        label=_("Secondary Virtual Circuit"),
    )

    fieldsets = (
        FieldSet(
            "status",
            "country_code",
            "start_number",
            "end_number",
            "type",
            "description",
            name=_("Number"),
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("primary_voice_circuit", name=_("Primary Circuit")),
                FieldSet("primary_virtual_circuit", name=_("Primary Virtual Circuit")),
            ),
            name=_("Primary Circuit"),
        ),
         FieldSet(
            TabbedGroups(
                FieldSet("secondary_voice_circuit", name=_("Secondary Circuit")),
                FieldSet("secondary_virtual_circuit", name=_("Secondary Virtual Circuit")),
            ),
            name=_("Secondary Circuit"),
        ),
        FieldSet(
            "tenant_group",
            "tenant",
            name=_("Tenancy"),
        ),
        FieldSet(
            "tags",
            name=_("Tags"),
        ),
    )

    class Meta:
        model = PhoneNumberRange
        fields = [
            "status",
            "description",
            "country_code",
            "start_number",
            "end_number",
            "primary_voice_circuit",
            "primary_virtual_circuit",
            "secondary_voice_circuit",
            "secondary_virtual_circuit",
            "type",
            "tenant_group",
            "tenant",
            "tags",
        ]


class PhoneNumberRangeFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = PhoneNumberRange
    fieldsets = (
        FieldSet("start_number", "country_code", "region", "type"),
        FieldSet("q", "filter_id", "tag"),
    )

    tag = TagFilterField(model)

    start_number = forms.CharField(label=_("Start number"), required=False)

    country_code = forms.MultipleChoiceField(label=_("Country code"), required=False, choices=PhoneCountryCodeChoises)
    type = forms.MultipleChoiceField(label=_("Type"), required=False, choices=PhoneRangeTypeChoices)


class PhoneNumberRangeBulkEditForm(NetBoxModelBulkEditForm):
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)

    type = forms.MultipleChoiceField(label=_("Type"), required=False, choices=PhoneRangeTypeChoices)

    status = forms.MultipleChoiceField(label=_("Status"), required=False, choices=PhoneNumberStatusChoises)

    primary_voice_circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all(),
        required=False,
        selector=True,
        label=_("Primary Circuit"),
    )

    primary_virtual_circuit = DynamicModelChoiceField(
        queryset=VirtualCircuit.objects.all(),
        required=False,
        selector=True,
        label=_("Primary Virtual Circuit"),
    )

    secondary_voice_circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all(),
        required=False,
        selector=True,
        label=_("Secondary Circuit"),
    )

    secondary_virtual_circuit = DynamicModelChoiceField(
        queryset=VirtualCircuit.objects.all(),
        required=False,
        selector=True,
        label=_("Secondary Virtual Circuit"),
    )

    description = forms.CharField(max_length=200, required=False)

    model = PhoneNumberRange

    fieldsets = (
        FieldSet(
            "status",
            "type",
            "description",
            name=_("Number"),
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("primary_voice_circuit", name=_("Primary Circuit")),
                FieldSet("primary_virtual_circuit", name=_("Primary Virtual Circuit")),
            ),
            name=_("Primary Circuit"),
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("secondary_voice_circuit", name=_("Secondary Circuit")),
                FieldSet("secondary_virtual_circuit", name=_("Secondary Virtual Circuit")),
            ),
            name=_("Secondary Circuit"),
        ),
        FieldSet(
            "tenant_group",
            "tenant",
            name=_("Tenancy"),
        ),       
    )

    nullable_fields = [ 
        "tenant"
    ]


class PhoneNumberForm(TenancyForm, NetBoxModelForm):

    primary_device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_("Device"),
    )
    primary_vm = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        selector=True,
        label=_("Virtual Machine"),
    )

    region_id = DynamicModelMultipleChoiceField(queryset=Region.objects.all(), required=False, label=_("Region"))

    secondary_device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_("Device"),
    )
    secondary_vm = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        selector=True,
        label=_("Virtual Machine"),
    )

    primary_voice_circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all(),
        required=False,
        selector=True,
        label=_("Primary Circuit"),
    )

    primary_virtual_circuit = DynamicModelChoiceField(
        queryset=VirtualCircuit.objects.all(),
        required=False,
        selector=True,
        label=_("Primary Virtual Circuit"),
    )

    secondary_voice_circuit = DynamicModelChoiceField(
        queryset=Circuit.objects.all(),
        required=False,
        selector=True,
        label=_("Secondary Circuit"),
    )

    secondary_virtual_circuit = DynamicModelChoiceField(
        queryset=VirtualCircuit.objects.all(),
        required=False,
        selector=True,
        label=_("Secondary Virtual Circuit"),
    )

    number_routing_ref = forms.CharField(
        required=False,
        label=_("Number Routing Reference"),
    )

    incoming_dialpeer = forms.CharField(
        required=False,
        label=_("Incoming dialpeer"),
    )

    outgoining_dialpeer = forms.CharField(
        required=False,
        label=_("Outgoining dialpeer"),
    )

    fieldsets = (
        FieldSet(
            "number",
            "status",
            "country_code",
            "sim",
            "type",
            "region",
            "description",
            "number_routing_ref",
            name=_("Number"),
        ),
        FieldSet(
            "incoming_dialpeer",
            "outgoining_dialpeer",
            name=_("dialpeer"),
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("primary_voice_circuit", name=_("Primary Circuit")),
                FieldSet("primary_virtual_circuit", name=_("Primary Virtual Circuit")),
            ),
            name=_("Primary Circuit"),
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("secondary_voice_circuit", name=_("Secondary Circuit")),
                FieldSet("secondary_virtual_circuit", name=_("Secondary Virtual Circuit")),
            ),
            name=_("Secondary Circuit"),
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("primary_device", name=_("Device")),
                FieldSet("primary_vm", name=_("Virtual Machine")),
            ),
            name=_("Master PBX"),
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("secondary_device", name=_("Device")),
                FieldSet("secondary_vm", name=_("Virtual Machine")),
            ),
            name=_("Secondary PBX"),
        ),
        FieldSet(
            "tenant_group",
            "tenant",
            name=_("Tenancy"),
        ),
        FieldSet(
            "tags",
            name=_("Tags"),
        ),
    )

    class Meta:
        model = PhoneNumber
        fields = [
            "number",
            "status",
            "description",
            "number_routing_ref",
            "country_code",
            "primary_voice_circuit",
            "primary_virtual_circuit",
            "secondary_voice_circuit",
            "secondary_virtual_circuit",
            "sim",
            "type",
            "primary_device",
            "primary_vm",
            "secondary_device",
            "secondary_vm",
            "incoming_dialpeer",
            "outgoining_dialpeer",
            "tenant_group",
            "tenant",
            "region",
            "tags",
        ]
    

class PhoneNumberFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = PhoneNumber
    fieldsets = (
        FieldSet(
            "number",
            "country_code",
            "incoming_dialpeer",
            "outgoining_dialpeer",
            "region",
            "primary_voice_circuit",
            "primary_virtual_circuit",
            "secondary_voice_circuit",
            "secondary_virtual_circuit",
            "type",
            "status",
        ),
        FieldSet("tenant_group_id", "tenant_id", name=_("Tenant")),
        FieldSet("q", "filter_id", "tag"),
    )

    tag = TagFilterField(model)

    number = forms.CharField(label=_("Number"), required=False)

    country_code = forms.MultipleChoiceField(label=_("Country code"), required=False, choices=PhoneCountryCodeChoises)

    status = forms.MultipleChoiceField(label=_("Status"), required=False, choices=PhoneNumberStatusChoises)

    type = forms.MultipleChoiceField(label=_("Type"), required=False, choices=PhoneRangeTypeChoices)

    incoming_dialpeer = forms.CharField(label=_("Incoming Dialpeer"), required=False)
    outgoining_dialpeer = forms.CharField(label=_("Outgoiging Dialpeer"), required=False)

    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(), required=False, null_option="None", label=_("Region")
    )

    primary_voice_circuit = DynamicModelMultipleChoiceField(
        queryset=Circuit.objects.all(), required=False, null_option="None", label=_("Primary Circuit")
    )
    primary_virtual_circuit = DynamicModelMultipleChoiceField(
        queryset=VirtualCircuit.objects.all(), required=False, null_option="None", label=_(" PrimaryVirtual Circuit")
    )

    secondary_voice_circuit = DynamicModelMultipleChoiceField(
        queryset=Circuit.objects.all(), required=False, null_option="None", label=_("Secondary Circuit")
    )
    secondary_virtual_circuit = DynamicModelMultipleChoiceField(
        queryset=VirtualCircuit.objects.all(), required=False, null_option="None", label=_("Secondary Virtual Circuit")
    )


class PhoneNumberImportForm(NetBoxModelImportForm):

    tenant = CSVModelChoiceField(
        label=_("Tenant"),
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Assigned tenant"),
    )

    region = CSVModelChoiceField(
        label=_("Region"),
        queryset=Region.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Assigned region"),
    )

    status = CSVChoiceField(label=_("Status"), choices=PhoneNumberStatusChoises, help_text=_("Operational status"))

    type = CSVChoiceField(label=_("Type"), choices=PhoneRangeTypeChoices, help_text=_("Operational status"))

    primary_device = CSVModelChoiceField(
        label=_("Primary Device"),
        queryset=Device.objects.all(),
        required=False,
        to_field_name="name",
    )

    primary_vm = CSVModelChoiceField(
        label=_("Primary VM"),
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name="name",
    )

    secondary_device = CSVModelChoiceField(
        label=_("Secondary Device"),
        queryset=Device.objects.all(),
        required=False,
        to_field_name="name",
    )

    secondary_vm = CSVModelChoiceField(
        label=_("Secondary VM"),
        queryset=VirtualMachine.objects.all(),
        required=False,
        to_field_name="name",
    )

    primary_voice_circuit = CSVModelChoiceField(
        label=_("Primary Circuit"),
        queryset=Circuit.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Assigned primary circuit"),
    )

    primary_virtual_circuit = CSVModelChoiceField(
        label=_("Primary Virtual Circuit"),
        queryset=VirtualCircuit.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Assigned primary virtual circuit"),
    )


    secondary_voice_circuit = CSVModelChoiceField(
        label=_("Primary Circuit"),
        queryset=Circuit.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Assigned secondary circuit"),
    )

    secondary_virtual_circuit = CSVModelChoiceField(
        label=_("Primary Virtual Circuit"),
        queryset=VirtualCircuit.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Assigned secondary virtual circuit"),
    )

    class Meta:
        model = PhoneNumber

        fields = (
            "tenant",
            "description",
            "number",
            "country_code",
            "incoming_dialpeer",
            "outgoining_dialpeer",
            "region",
            "status",
            "type",
            "primary_voice_circuit",
            "primary_virtual_circuit",
            "secondary_voice_circuit",
            "secondary_virtual_circuit",
            "primary_device",
            "primary_vm",
            "secondary_device",
            "secondary_vm",
            "tags",
        )


class PhoneNumberBulkEditForm(NetBoxModelBulkEditForm):
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)

    type = forms.MultipleChoiceField(label=_("Type"), required=False, choices=PhoneRangeTypeChoices)

    status = forms.MultipleChoiceField(label=_("Status"), required=False, choices=PhoneNumberStatusChoises)

    region = DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(), required=False, null_option="None", label=_("Region")
    )

    primary_voice_circuit = DynamicModelMultipleChoiceField(
        queryset=Circuit.objects.all(), required=False, null_option="None", label=_("Primary Circuit")
    )

    primary_virtual_circuit = DynamicModelChoiceField(
        queryset=VirtualCircuit.objects.all(),
        required=False,
        selector=True,
        label=_("Primary Virtual Circuit"),
    )

    secondary_voice_circuit = DynamicModelMultipleChoiceField(
        queryset=Circuit.objects.all(), required=False, null_option="None", label=_("Secondary Circuit")
    )

    secondary_virtual_circuit = DynamicModelChoiceField(
        queryset=VirtualCircuit.objects.all(),
        required=False,
        selector=True,
        label=_("Secondary Virtual Circuit"),
    )

    incoming_dialpeer = forms.CharField(label=_("Incoming dialpeer"), required=False)
    outgoining_dialpeer = forms.CharField(label=_("Outgoiging Dialpeer"), required=False)

    primary_device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_("Device"),
    )
    primary_vm = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        selector=True,
        label=_("Virtual Machine"),
    )

    secondary_device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_("Device"),
    )
    secondary_vm = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        selector=True,
        label=_("Virtual Machine"),
    )

    description = forms.CharField(max_length=200, required=False)

    model = PhoneNumber

    fieldsets = (
        FieldSet(
            "status",
            "country_code",
            "type",
            "region",
            "description",
            "number_routing_ref",
            name=_("Number"),
        ),
        FieldSet(
            "incoming_dialpeer",
            "outgoining_dialpeer",
            name=_("dialpeer"),
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("primary_voice_circuit", name=_("Primary Circuit")),
                FieldSet("primary_virtual_circuit", name=_("Primary Virtual Circuit")),
            ),
            name=_("Primary Circuit"),
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("secondary_voice_circuit", name=_("Secondary Circuit")),
                FieldSet("secondary_virtual_circuit", name=_("Secondary Virtual Circuit")),
            ),
            name=_("Secondary Circuit"),
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("primary_device", name=_("Device")),
                FieldSet("primary_vm", name=_("Virtual Machine")),
            ),
            name=_("Master PBX"),
        ),
        FieldSet(
            TabbedGroups(
                FieldSet("secondary_device", name=_("Device")),
                FieldSet("secondary_vm", name=_("Virtual Machine")),
            ),
            name=_("Secondary PBX"),
        ),
        FieldSet(
            "tenant_group",
            "tenant",
            name=_("Tenancy"),
        ),
     )

    nullable_fields = [ 
        "tenant"
    ]



class SimForm(TenancyForm, NetBoxModelForm):

    provider = DynamicModelChoiceField(
        label=_("Provider"), queryset=Provider.objects.all(), selector=True, quick_add=True
    )

    provider_account = DynamicModelChoiceField(
        label=_("Provider account"),
        queryset=ProviderAccount.objects.all(),
        required=False,
        query_params={
            "provider_id": "$provider",
        },
    )

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_("Device"),
    )

    fieldsets = (
        FieldSet(
            "sim_id",
            "iccid",
            "msisdn",
            "pin",
            "puk",
            "volume_limit",
            "description",
            "device",
            "provider",
            "provider_account",
            name=_("SIM"),
        ),
        FieldSet(
            "tenant_group",
            "tenant",
            name=_("Tenancy"),
        ),
        FieldSet(
            "tags",
            name=_("Tags"),
        ),
    )

    class Meta:
        model = Sim
        fields = [
            "sim_id",
            "iccid",
            "msisdn",
            "pin",
            "puk",
            "volume_limit",
            "description",
            "tenant_group",
            "tenant",
            "provider",
            "provider_account",
            "device",
            "tags",
        ]


class SimFilterForm(TenancyFilterForm, NetBoxModelFilterSetForm):
    model = Sim
    fieldsets = (
        FieldSet("sim_id", "ICCID", "MSISDN"),
        FieldSet('provider_id', 'provider_account_id', name=_('Provider')),
        FieldSet('device'),
        FieldSet("q", "filter_id", "tag"),
    )

    tag = TagFilterField(model)

    sim_id = forms.CharField(label=_("SIM ID"), required=False)

    iccid = forms.CharField(label=_("ICCID"), required=False)

    msisdn = forms.CharField(label=_("MSISDN"), required=False)

    provider_id = DynamicModelMultipleChoiceField(
        queryset=Provider.objects.all(),
        required=False,
        label=_('Provider')
    )
    provider_account_id = DynamicModelMultipleChoiceField(
        queryset=ProviderAccount.objects.all(),
        required=False,
        query_params={
            'provider_id': '$provider_id'
        },
        label=_('Provider account')
    )

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        selector=True,
        label=_("Device"),
    )

    


class SimBulkEditForm(NetBoxModelBulkEditForm):
    description = forms.CharField(max_length=200, required=False)
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)

    provider = DynamicModelChoiceField(
        label=_("Provider"), queryset=Provider.objects.all(), selector=True, quick_add=True, required=False
    )

    provider_account = DynamicModelChoiceField(
        label=_("Provider account"),
        queryset=ProviderAccount.objects.all(),
        required=False,
        query_params={
            "provider_id": "$provider",
        },
    )

    model = Sim

    fieldsets = (
        FieldSet(            
            "description",
            "provider",
            "provider_account",
            name=_("SIM"),
        ),
        FieldSet(
            "tenant_group",
            "tenant",
            name=_("Tenancy"),
        ),
    )

    nullable_fields = [
        "tenant",
        "description",
        "provider",
        "provider_account",
    ]


class SimImportForm(NetBoxModelImportForm):

    tenant = CSVModelChoiceField(
        label=_("Tenant"),
        queryset=Tenant.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Assigned tenant name"),
    )

    device = CSVModelChoiceField(
        label=_("Device"),
        queryset=Device.objects.all(),
        required=False,
        to_field_name="name",
        help_text=_("Assigned device name"),
    )

    provider = CSVModelChoiceField(
        label=_("Provider"), queryset=Provider.objects.all(), to_field_name="name", help_text=_("Assigned provider")
    )
    provider_account = CSVModelChoiceField(
        label=_("Provider account"),
        queryset=ProviderAccount.objects.all(),
        to_field_name="name",
        help_text=_("Assigned provider account"),
        required=False,
    )

    class Meta:
        model = Sim
        fields = (
            "sim_id",
            "iccid",
            "msisdn",
            "pin",
            "puk",
            "volume_limit",
            "description",
            "tenant",
            "provider",
            "provider_account",
            "device"
        )


class SimAdminForm(NetBoxModelForm):

    fieldsets = (
        FieldSet(
            "sim",
            "ki",
            "opc",
            "admin_key",
            "mapped_imei",
            name=_("SIM"),
        ),
    )

    class Meta:
        model = SimAdmin
        fields = [
            "sim",
            "ki",
            "opc",
            "admin_key",
            "mapped_imei",
        ]


class SimAdminFilterForm(NetBoxModelFilterSetForm):
    model = SimAdmin
    fieldsets = (FieldSet("q", "filter_id", "tag"),)

    tag = TagFilterField(model)


class SimAdminImportForm(NetBoxModelImportForm):

    sim = CSVModelChoiceField(
        label=_("sim"),
        queryset=Sim.objects.all(),
        required=True,
        to_field_name="sim_id",
        help_text=_("Assigned sim sim_id"),
    )

    class Meta:
        model = SimAdmin
        fields = ("sim", "ki", "opc", "admin_key", "mapped_imei")
