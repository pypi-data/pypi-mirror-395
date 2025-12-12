from netbox.plugins import PluginConfig


class NetBoxInterfaceViewConfig(PluginConfig):
    name = 'netbox_interface_view'
    verbose_name = 'NetBox Interface View'
    description = 'NetBox Plugin for viewing interfaces in a grid layout with VLAN color-coding'
    version = '0.2.11'
    base_url = 'interface-view'
    min_version = '3.5.0'


config = NetBoxInterfaceViewConfig
