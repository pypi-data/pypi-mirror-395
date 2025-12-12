from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import RegexValidator
from netbox.models import NetBoxModel
from taggit.managers import TaggableManager
from extras.models import TaggedItem
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError

from .choices import PhoneRangeTypeChoices, PhoneNumberStatusChoises, PhoneCountryCodeChoises


number_validator = RegexValidator(
    r"^\+?[0-9A-D\#\*]*$",
    "Numbers can only contain: leading +, digits 0-9; chars A, B, C, D; # and *"
)

class PhoneNumberRange(NetBoxModel):
    country_code = models.CharField(
        verbose_name=_('Country code'),
        max_length=50,
        choices=PhoneCountryCodeChoises,
        default=PhoneCountryCodeChoises.COUNTRY_BELGIUM,
        help_text=_('The country code of this Number')
    )
     
    start_number = models.PositiveIntegerField(
        help_text=_("Only digits without coutry code")
    )
    end_number = models.PositiveIntegerField(
        help_text=_("Only digits without coutry code")
    )

    size = models.PositiveIntegerField(
        verbose_name=_('size'),
        editable=False
    )

    status = models.CharField(
        verbose_name=_('status'),
        max_length=50,
        choices=PhoneNumberStatusChoises,
        default=PhoneNumberStatusChoises.STATUS_ACTIVE,
        help_text=_('The operational status of this Number')
    )

    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='phonenumberrange',
        blank=True,
        null=True
    )

    description = models.CharField(
        max_length=255,
        blank = True,
    )

    type = models.CharField(
        max_length=50,
        choices=PhoneRangeTypeChoices,
        default=PhoneRangeTypeChoices.TYPE_FIXED
    )

    primary_voice_circuit = models.ForeignKey(
        to="circuits.Circuit",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="phonenumberranges_circuit"
    )

    primary_virtual_circuit = models.ForeignKey(
        to="circuits.VirtualCircuit",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="phonenumberranges_virtualcircuit"
    )

    secondary_voice_circuit = models.ForeignKey(
        to="circuits.Circuit",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="phonenumberranges_circuit_secondary"
    )

    secondary_virtual_circuit = models.ForeignKey(
        to="circuits.VirtualCircuit",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="phonenumberranges_virtualcircuit_secondary"
    )

    region = models.ForeignKey(
        to="dcim.Region",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="phonenumberranges_region"
    )

    tags = TaggableManager(through=TaggedItem)

    class Meta:
        ordering = ['pk']

    def clean(self):
        super().clean()

        if self.start_number and self.end_number:
            if not self.end_number > self.start_number:
                raise ValidationError({
                    'end_number': _(
                        "Ending address must be greater than the starting address ({start_number})"
                    ).format(start_number=self.start_number)
                })

    def save(self, *args, **kwargs):
        self.size = int(self.end_number - self.start_number)
        super().save(*args, **kwargs)

    def __str__(self):
        return ("{}{} to {}{}".format(self.country_code, self.start_number, self.country_code, self.end_number))
    
    def get_child_numbers(self):
        return PhoneNumber.objects.filter(
            number__gte=self.start_number,
            number__lte=self.end_number,
            country_code=self.country_code
        )



class PhoneNumber(NetBoxModel):
    number = models.PositiveIntegerField(
        help_text=_("Only digits without coutry code")
    )

    country_code = models.CharField(
        verbose_name=_('Country code'),
        max_length=50,
        choices=PhoneCountryCodeChoises,
        default=PhoneCountryCodeChoises.COUNTRY_BELGIUM,
        help_text=_('The country code of this Number')
    )

    incoming_dialpeer  = models.CharField(max_length=32, blank=True)
    outgoining_dialpeer  = models.CharField(max_length=32,blank=True)

    number_routing_ref = models.CharField(
        max_length=255,
        blank = True,
        help_text=_('Link to git')
    )

    description = models.CharField(
        max_length=255,
        blank = True,
    )

    status = models.CharField(
        verbose_name=_('status'),
        max_length=50,
        choices=PhoneNumberStatusChoises,
        default=PhoneNumberStatusChoises.STATUS_ACTIVE,
        help_text=_('The operational status of this Number')
    )

    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='phonenumbers',
        blank=True,
        null=True
    )

    region = models.ForeignKey(
        to="dcim.Region",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="phonenumbers_region"
    )

    primary_device = models.ForeignKey(
        to="dcim.Device",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="phonenumbers_device"
    )

    primary_vm = models.ForeignKey(
        to="virtualization.Virtualmachine",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="phonenumbers_vm"
    )

    secondary_device = models.ForeignKey(
        to="dcim.Device",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="phonenumbers_device_sec"
    )

    secondary_vm = models.ForeignKey(
        to="virtualization.Virtualmachine",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="phonenumbers_vm_sec"
    )

    primary_voice_circuit = models.ForeignKey(
        to="circuits.Circuit",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="phonenumbers_circuit"
    )

    primary_virtual_circuit = models.ForeignKey(
        to="circuits.VirtualCircuit",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="phonenumbers_virtualcircuit"
    )

    secondary_voice_circuit = models.ForeignKey(
        to="circuits.Circuit",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="phonenumbers_circuit_secondary"
    )

    secondary_virtual_circuit = models.ForeignKey(
        to="circuits.VirtualCircuit",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="phonenumbers_virtualcircuit_secondary"
    )

    sim = models.ForeignKey(
        to="phone_management_plugin.Sim",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="sim_number"
    )

    type = models.CharField(
        max_length=50,
        choices=PhoneRangeTypeChoices,
        default=PhoneRangeTypeChoices.TYPE_FIXED
    ) 


    tags = TaggableManager(through=TaggedItem)

    class Meta:
        ordering = ('number', 'pk')

        constraints = [
            models.UniqueConstraint(
                fields=['number', 'country_code'],
                name='unique_number_country_code'
            )
        ]

    def __str__(self):
        return ("{}{}".format(self.country_code, self.number))


    def clean(self):
        super().clean()

        if self.number:
            if self.primary_device is not None and self.primary_vm is not None:
                raise ValidationError(
                     _("Cannot both assign a vm and a device to an number")
                )
            
            if self.secondary_device is not None and self.secondary_vm is not None:
                raise ValidationError(
                     _("Cannot both assign a vm and a device to an number")
                )
            
            if self.primary_virtual_circuit is not None and self.primary_voice_circuit is not None:
                raise ValidationError(
                     _("Cannot both assign a circuit and a voice circuit to an number")
                )

            if self.secondary_virtual_circuit is not None and self.secondary_voice_circuit is not None:
                raise ValidationError(
                     _("Cannot both assign a circuit and a voice circuit to an number")
                )           


class Sim(NetBoxModel):

    sim_id = models.PositiveBigIntegerField(
        verbose_name="SIM ID",
        help_text=_("ID of the SIM"),
        unique=True
    )

    iccid =  models.DecimalField(
        verbose_name="ICCID",
        help_text=_("Integrated Circuit Card Identifier"),
        max_digits=30, 
        decimal_places=0
    )
    msisdn = models.PositiveBigIntegerField(
        verbose_name="MSISDN",
        help_text=_("Mobile Station International Subscriber Directory Number")
    )
    pin = models.PositiveIntegerField(
        verbose_name="PIN",
        help_text=_("PIN of the SIM card"),
        blank = True,
        null=True
        
    )
    puk = models.PositiveIntegerField(
        verbose_name="PUK",
        help_text=_("PUK of the SIM card"),
        blank = True,
        null=True
    )
    volume_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_('Volume in GBs, 0.00 for unlimited'),
        default=0
    )

    description = models.CharField(
        max_length=255,
        blank = True,
    )

    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='sim',
        blank=True,
        null=True
    )

    provider = models.ForeignKey(
        to='circuits.Provider',
        on_delete=models.PROTECT,
        related_name='circuitsim'
    )
    provider_account = models.ForeignKey(
        to='circuits.ProviderAccount',
        on_delete=models.PROTECT,
        related_name='circuitssim',
        blank=True,
        null=True
    )

    tags = TaggableManager(through=TaggedItem)

    device = models.ForeignKey(
        to="dcim.Device",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="sim_device"
    )

    prerequisite_models = (
        'circuits.Provider',
    )

    class Meta:
        ordering = ('sim_id', 'pk')
        verbose_name = "SIM"
        verbose_name_plural = "SIMs"

    def __str__(self):
        return ("{}".format(self.sim_id))

class SimAdmin(NetBoxModel):

    sim = models.OneToOneField(
        verbose_name="SIM",
        to="phone_management_plugin.Sim",
        on_delete=models.PROTECT,
        related_name="sim_admin"
    )

    ki = models.CharField(
        verbose_name=_('Authentication Key'),
        max_length=50,
        help_text=_('Authentication Key'),
        blank=True,
        null=True
    )
    opc = models.CharField(
        verbose_name=_('Operator Code'),
        max_length=50,
        help_text=_('Operator Code'),
        blank=True,
        null=True
    )
    admin_key = models.CharField(
        verbose_name=_('Admin key'),
        max_length=50,
        help_text=_('Admin key'),
        blank=True,
        null=True
    )

    mapped_imei =  models.PositiveBigIntegerField(
        verbose_name="Mapped IMEI",
        help_text=_("IMEI of the connected device"),
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['pk']
        verbose_name = "SIM Private"
        verbose_name_plural = "SIMs Private"

    def __str__(self):
        return ("Admin conf SIM {}".format(self.sim.sim_id))