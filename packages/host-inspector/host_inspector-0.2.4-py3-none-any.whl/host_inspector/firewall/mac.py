def is_firewall_enabled() -> bool:
    """
    Returns True if the firewall is enabled, False otherwise.
    """
    return False  # Placeholder implementation


def get_firewall_rules(
    ports=None, direction=None, enabled_only=False, exclude_any_ports=False
):
    # TODO: Implement Mac firewall rules parsing
    return []


def get_firewall_info(
    ports=None,
    direction=None,
    enabled_only=False,
    exclude_any_ports=False,
) -> dict:
    """Return a dict of firewall info."""
    return {
        "enabled": is_firewall_enabled(),
        "status": "ON" if is_firewall_enabled() else "OFF",
        "rules": get_firewall_rules(
            ports=ports,
            direction=direction,
            enabled_only=enabled_only,
            exclude_any_ports=exclude_any_ports,
        ),
    }
