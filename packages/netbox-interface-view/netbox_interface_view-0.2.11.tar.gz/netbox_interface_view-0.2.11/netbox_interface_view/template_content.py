from netbox.plugins import PluginTemplateExtension
from django.urls import reverse
from django.utils.html import format_html


class DeviceInterfaceGridButton(PluginTemplateExtension):
    """Add Interface Grid View button to device pages"""
    
    models = ('dcim.device',)
    
    def buttons(self):
        """Add button to device detail page"""
        obj = self.context['object']
        url = reverse('plugins:netbox_interface_view:interface_grid', kwargs={'device_id': obj.pk})
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary" title="View Interface Grid">'
            '<i class="mdi mdi-view-grid"></i> View Interface Grid'
            '</a>',
            url
        )

class RackInterfaceGridButton(PluginTemplateExtension):
    """Add Interface Grid View button to rack pages"""
    
    models = ("dcim.rack",)
    
    def buttons(self):
        """Add button to rack detail page"""
        obj = self.context['object']
        url = reverse('plugins:netbox_interface_view:rack_interface_grid', kwargs={'rack_id': obj.pk})
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary" title="View Rack Interface Grid">'
            '<i class="mdi mdi-view-grid"></i> View Rack Interfaces'
            '</a>',
            url
        )


template_extensions = [DeviceInterfaceGridButton, RackInterfaceGridButton]
