from netbox.api.serializers import NetBoxModelSerializer
from tenancy.api.serializers_.tenants import TenantSerializer
from rest_framework import serializers
from netbox.api.fields import ChoiceField, ContentTypeField
from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from utilities.api import get_serializer_for_model
from django.db.models import Q
from circuits.api.serializers import ProviderAccountSerializer, ProviderSerializer

from phone_management_plugin.models import PhoneNumber, PhoneNumberRange, Sim, SimAdmin


class PhoneNumberRangeSerializer(NetBoxModelSerializer):
    class Meta:
        model = PhoneNumberRange

        fields = (
            "id",
            "url",
            "tags",
            "type",
            "status",
            "country_code",
            "start_number",
            "primary_voice_circuit",
            "primary_virtual_circuit",
            "secondary_voice_circuit",
            "secondary_virtual_circuit",
            "end_number",
            "created",
            "last_updated",
            "custom_fields",
            "tenant",
            "description",
            "size",
        )

        brief_fields = (
            "id",
            "url",
            "description",
        )

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:phone_management_plugin-api:phonenumberrange-detail"
    )

    tenant = TenantSerializer(
        nested=True,
        required=False,
        allow_null=True,
    )


class PhoneNumberSerializer(NetBoxModelSerializer):
    class Meta:
        model = PhoneNumber

        fields = (
            "id",
            "url",
            "number",
            "region",
            "description",
            "primary_device",
            "primary_vm",
            "country_code",
            "secondary_device",
            "secondary_vm",
            "number_routing_ref",
            "primary_voice_circuit",
            "primary_virtual_circuit",
            "secondary_voice_circuit",
            "secondary_virtual_circuit",
            "sim",
            "type",
            "tags",
            "status",
            "created",
            "last_updated",
            "custom_fields",
            "tenant",
        )

        brief_fields = (
            "id",
            "url",
            "number",
            "description",
        )

    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:phone_management_plugin-api:phonenumber-detail")

    tenant = TenantSerializer(
        nested=True,
        required=False,
        allow_null=True,
    )


class SimSerializer(NetBoxModelSerializer):

    provider = ProviderSerializer(nested=True)
    provider_account = ProviderAccountSerializer(nested=True, required=False, allow_null=True, default=None)

    class Meta:
        model = Sim

        fields = (
            "id",
            "url",
            "sim_id",
            "description",
            "iccid",
            "msisdn",
            "pin",
            "puk",
            "volume_limit",
            "tenant",
            "provider",
            "provider_account",
            "device",
        )

        brief_fields = (
            "id",
            "url",
        )

    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:phone_management_plugin-api:sim-detail")


class SimAdminSerializer(NetBoxModelSerializer):
    class Meta:
        model = SimAdmin

        fields = (
            "id",
            "url",
            "sim",
            "ki",
            "opc",
            "admin_key",
            "mapped_imei",
        )

        brief_fields = (
            "id",
            "url",
        )

    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:phone_management_plugin-api:simadmin-detail")
