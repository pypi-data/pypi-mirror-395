from rest_framework import serializers
from rest_framework.routers import APIRootView

from netbox.api.viewsets import NetBoxModelViewSet

from .serializers import PhoneNumberSerializer, PhoneNumberRangeSerializer, SimSerializer, SimAdminSerializer

from phone_management_plugin.models import PhoneNumber, PhoneNumberRange, Sim, SimAdmin
from phone_management_plugin.filtersets import PhoneNumberFilterSet, SimFilterSet, SimAdminFilterSet, PhoneNumberRangeFilterSet

class PhoneManagementPluginRootView(APIRootView):
    def get_view_name(self):
        return "PhoneManagementPlugin"


class PhoneNumberViewSet(NetBoxModelViewSet):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer
    filterset_class = PhoneNumberFilterSet

class PhoneNumberRangeViewSet(NetBoxModelViewSet):
    queryset = PhoneNumberRange.objects.all()
    serializer_class = PhoneNumberRangeSerializer
    filterset_class = PhoneNumberRangeFilterSet

class SimViewSet(NetBoxModelViewSet):
    queryset = Sim.objects.all()
    serializer_class = SimSerializer
    filterset_class = SimFilterSet

class SimAdminViewSet(NetBoxModelViewSet):
    queryset = SimAdmin.objects.all()
    serializer_class = SimAdminSerializer
    filterset_class = SimAdminFilterSet
