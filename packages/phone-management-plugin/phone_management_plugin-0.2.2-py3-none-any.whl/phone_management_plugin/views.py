from django.shortcuts import render
from .models import PhoneNumberRange, PhoneNumber, Sim, SimAdmin
from utilities.views import register_model_view, ViewTab
from netbox.views import generic
from . import filtersets
from . import forms
from . import tables
from django.utils.translation import gettext_lazy as _

# PhoneNumberRange
@register_model_view(PhoneNumberRange, 'list', path='', detail=False)
class PhoneNumberRangeObjectListView(generic.ObjectListView):
    queryset = PhoneNumberRange.objects.all()
    filterset = filtersets.PhoneNumberRangeFilterSet
    filterset_form = forms.PhoneNumberRangeFilterForm
    table = tables.PhoneNumberRangeTable

@register_model_view(PhoneNumberRange)
class PhoneNumberRangeView(generic.ObjectView):
    queryset = PhoneNumberRange.objects.all()

@register_model_view(PhoneNumberRange, 'add', detail=False)
@register_model_view(PhoneNumberRange, 'edit')
class PhoneNumberRangeEditView(generic.ObjectEditView):
    queryset = PhoneNumberRange.objects.all()
    form = forms.PhoneNumberRangeForm

@register_model_view(PhoneNumberRange, "delete")
class PhoneNumberRangeDeleteView(generic.ObjectDeleteView):
    queryset = PhoneNumberRange.objects.all()

@register_model_view(PhoneNumberRange, 'bulk_delete', path='delete', detail=False)
class PhoneNumberRangeBulkDeleteView(generic.BulkDeleteView):
    queryset = PhoneNumberRange.objects.all()
    filterset = filtersets.PhoneNumberRangeFilterSet
    table = tables.PhoneNumberRangeTable

@register_model_view(PhoneNumberRange, 'bulk_edit', path='edit', detail=False)
class PhoneNumberRangeBulkEditView(generic.BulkEditView):
    queryset = PhoneNumberRange.objects.all()
    filterset = filtersets.PhoneNumberRangeFilterSet
    table = tables.PhoneNumberRangeTable
    form = forms.PhoneNumberRangeBulkEditForm

@register_model_view(PhoneNumberRange, 'phonenumberranges', path='phonenumberranges')
class IPRangeIPAddressesView(generic.ObjectChildrenView):
    queryset = PhoneNumberRange.objects.all()
    child_model = PhoneNumber
    table = tables.PhoneNumberTable
    filterset = filtersets.PhoneNumberRangeFilterSet
    filterset_form = forms.PhoneNumberRangeFilterForm
    tab = ViewTab(
        label=_('Child Numbers'),
        badge=lambda x: x.get_child_numbers().count(),
        permission='ipam.view_ipaddress',
        weight=500
    )

    def get_children(self, request, parent):
        return parent.get_child_numbers().restrict(request.user, 'view')

# PhoneNumber
@register_model_view(PhoneNumber, 'list', path='', detail=False)
class PhoneNumberObjectListView(generic.ObjectListView):
    queryset = PhoneNumber.objects.all()
    filterset = filtersets.PhoneNumberFilterSet
    filterset_form = forms.PhoneNumberFilterForm
    table = tables.PhoneNumberTable

@register_model_view(PhoneNumber)
class PhoneNumberView(generic.ObjectView):
    queryset = PhoneNumber.objects.all()

@register_model_view(PhoneNumber, 'add', detail=False)
@register_model_view(PhoneNumber, 'edit')
class PhoneNumberEditView(generic.ObjectEditView):
    queryset = PhoneNumber.objects.all()
    form = forms.PhoneNumberForm

@register_model_view(PhoneNumber, "delete")
class PhoneNumberDeleteView(generic.ObjectDeleteView):
    queryset = PhoneNumber.objects.all()

@register_model_view(PhoneNumber, 'bulk_import', path='import', detail=False)
class PrefixBulkImportView(generic.BulkImportView):
    queryset = PhoneNumber.objects.all()
    model_form = forms.PhoneNumberImportForm

@register_model_view(PhoneNumber, 'bulk_delete', path='delete', detail=False)
class PhoneNumberBulkDeleteView(generic.BulkDeleteView):
    queryset = PhoneNumber.objects.all()
    filterset = filtersets.PhoneNumberFilterSet
    table = tables.PhoneNumberTable

@register_model_view(PhoneNumber, 'bulk_edit', path='edit', detail=False)
class PhoneNumberBulkEditView(generic.BulkEditView):
    queryset = PhoneNumber.objects.all()
    filterset = filtersets.PhoneNumberFilterSet
    table = tables.PhoneNumberTable
    form = forms.PhoneNumberBulkEditForm


# Sim
@register_model_view(Sim, 'list', path='', detail=False)
class SimObjectListView(generic.ObjectListView):
    queryset = Sim.objects.all()
    filterset = filtersets.SimFilterSet
    filterset_form = forms.SimFilterForm
    table = tables.SimTable

@register_model_view(Sim)
class SimView(generic.ObjectView):
    queryset = Sim.objects.all()

    def get_extra_context(self, request, instance):
        print(instance.id)

        try:
            simadmin = SimAdmin.objects.restrict(request.user, 'view').get(sim__id=instance.id)
        except SimAdmin.DoesNotExist:
            simadmin = None

        return {
            'sim_private': simadmin,
        }

@register_model_view(Sim, 'add', detail=False)
@register_model_view(Sim, 'edit')
class SimEditView(generic.ObjectEditView):
    queryset = Sim.objects.all()
    form = forms.SimForm

@register_model_view(Sim, 'bulk_edit', path='edit', detail=False)
class SimBulkEditView(generic.BulkEditView):
    queryset = Sim.objects.all()
    form = forms.SimBulkEditForm
    filterset = filtersets.SimFilterSet
    table = tables.SimTable

@register_model_view(Sim, "delete")
class SimDeleteView(generic.ObjectDeleteView):
    queryset = Sim.objects.all()

@register_model_view(Sim, 'bulk_import', path='import', detail=False)
class SimImportView(generic.BulkImportView):
    queryset = Sim.objects.all()
    model_form = forms.SimImportForm

@register_model_view(Sim, 'bulk_delete', path='delete', detail=False)
class SimBulkDeleteView(generic.BulkDeleteView):
    queryset = Sim.objects.all()
    filterset = filtersets.SimFilterSet
    table = tables.SimTable

# SimAdmin
@register_model_view(SimAdmin, 'list', path='', detail=False)
class SimAdminObjectListView(generic.ObjectListView):
    queryset = SimAdmin.objects.all()
    filterset = filtersets.SimAdminFilterSet
    filterset_form = forms.SimAdminFilterForm
    table = tables.SimAdminTable

@register_model_view(SimAdmin)
class SimAdminView(generic.ObjectView):
    queryset = SimAdmin.objects.all()

@register_model_view(SimAdmin, 'add', detail=False)
@register_model_view(SimAdmin, 'edit')
class SimAdminEditView(generic.ObjectEditView):
    queryset = SimAdmin.objects.all()
    form = forms.SimAdminForm

@register_model_view(SimAdmin, "delete")
class SimAdminDeleteView(generic.ObjectDeleteView):
    queryset = SimAdmin.objects.all()

@register_model_view(SimAdmin, 'bulk_import', path='import', detail=False)
class SimAdminImportView(generic.BulkImportView):
    queryset = SimAdmin.objects.all()
    model_form = forms.SimAdminImportForm

@register_model_view(SimAdmin, 'bulk_delete', path='delete', detail=False)
class SimAdminBulkDeleteView(generic.BulkDeleteView):
    queryset = SimAdmin.objects.all()
    filterset = filtersets.SimAdminFilterSet
    table = tables.SimAdminTable