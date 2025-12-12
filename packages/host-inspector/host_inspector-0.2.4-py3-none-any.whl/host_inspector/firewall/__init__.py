from host_inspector.utils.importutils import get_platform_module

platform_module = get_platform_module(__name__)

get_firewall_info = platform_module.get_firewall_info
is_firewall_enabled = platform_module.is_firewall_enabled
