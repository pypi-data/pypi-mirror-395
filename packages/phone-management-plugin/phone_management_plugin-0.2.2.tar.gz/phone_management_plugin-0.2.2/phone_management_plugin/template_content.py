import logging
from netbox.plugins import PluginTemplateExtension
from . import models

class SimDeviceInfoView(PluginTemplateExtension):
    models = ["dcim.device"]

    def right_page(self):
        try:
            simcards = models.Sim.objects.filter(
                device__id = self.context["object"].id
            ).select_related().order_by('sim_id')
          
        except:
            simcards = None
           
            return ""
        
        return self.render(
            "phone_management_plugin/inc/device_info.html",
            extra_context={"simcards": simcards},
        )


template_extensions = [ 
    SimDeviceInfoView
]