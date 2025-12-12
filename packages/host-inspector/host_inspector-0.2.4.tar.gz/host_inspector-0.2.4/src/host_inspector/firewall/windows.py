import contextlib
import logging
import re
import subprocess

logger = logging.getLogger(__name__)


def check_firewall_status():
    """
    Prints firewall status (overall ON/OFF).
    Returns True if firewall is enabled in at least one profile.
    """
    status = is_firewall_enabled()
    return status["overall"]


def is_firewall_enabled():
    """
    Returns a dict with firewall status for domain, private, public, and overall.
    Uses `netsh advfirewall show allprofiles`.

    Example:
        {'domain': True, 'private': True, 'public': False, 'overall': True}
    """

    command = ["netsh", "advfirewall", "show", "allprofiles"]
    try:
        result = subprocess.run(  # noqa: S603
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",
        )
        output = result.stdout
    except subprocess.CalledProcessError:
        return {"domain": None, "private": None, "public": None, "overall": None}

    profiles = {"domain": False, "private": False, "public": False}

    # Regex to capture each profile's "State"
    for profile in profiles:
        match = re.search(
            rf"{profile}\s*profile settings:.*?state\s*on",
            output,
            re.IGNORECASE | re.DOTALL,
        )
        profiles[profile] = bool(match)

    # Overall is ON if any profile is ON
    profiles["overall"] = any(profiles.values())
    return profiles


def get_firewall_rules(
    ports=None, direction=None, enabled_only=False, exclude_any_ports=False
):
    command = ["netsh", "advfirewall", "firewall", "show", "rule", "name=all"]
    if direction:
        command.extend([f"dir={direction}"])

    try:
        result = subprocess.run(  # noqa: S603
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
            timeout=30,
        )
        return parse_firewall_output(
            result.stdout, ports, enabled_only, exclude_any_ports
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        logger.exception("Error executing command")
        return []


def parse_firewall_output(
    output, ports_filter=None, enabled_only=False, exclude_any_ports=False
):
    rules = []
    ports_set = {str(p) for p in ports_filter} if ports_filter else None

    rule_blocks = re.split(r"\n(?=Rule Name:)", output)
    for block in rule_blocks:
        if "Rule Name:" not in block:
            continue

        rule = parse_single_rule_block(block)
        if not rule:
            continue

        # Skip rules that are not enabled if `enabled_only` is True
        if enabled_only and not rule.get("enabled", False):
            continue

        # Handle port filtering
        rule_port = rule.get("port")

        # Exclude "Any" ports if requested
        if exclude_any_ports and rule_port == "Any":
            continue

        # Filter by specific ports if provided
        if ports_set and rule_port != "Any":
            # Extract all numeric ports from the rule (handles ranges, lists, etc.)
            rule_ports = extract_ports_from_rule(rule_port)
            if not any(str(port) in ports_set for port in rule_ports):
                continue

        rules.append(rule)

    return rules


def extract_ports_from_rule(port_spec):  # noqa: PLR0911
    """Extract all individual ports from a port specification (ranges, lists, etc.)"""
    if not port_spec or port_spec == "Any":
        return []

    # If it's a simple integer, return it
    if isinstance(port_spec, int):
        return [port_spec]

    # If it's a string that can be converted to int, return it
    if isinstance(port_spec, str) and port_spec.isdigit():
        return [int(port_spec)]

    # Handle port ranges (e.g., "1000-2000")
    if isinstance(port_spec, str) and "-" in port_spec:
        try:
            start, end = map(int, port_spec.split("-"))
            return list(range(start, end + 1))
        except ValueError:
            return []

    # Handle comma-separated lists (e.g., "80,443,8080")
    if isinstance(port_spec, str) and "," in port_spec:
        ports = []
        for part in port_spec.split(","):
            part_stripped = part.strip()
            if part_stripped.isdigit():
                ports.append(int(part_stripped))
            elif "-" in part_stripped:  # Handle ranges within lists
                ports.extend(extract_ports_from_rule(part_stripped))
        return ports

    # If it's a service name or other non-numeric value, return empty
    return []


def parse_single_rule_block(block):
    """
    Parse a single rule block into a dictionary.
    """
    patterns = {
        "name": r"Rule Name:\s*(.+?)(?:\n|$)",
        "direction": r"Direction:\s*(.+?)(?:\n|$)",
        "action": r"Action:\s*(.+?)(?:\n|$)",
        "protocol": r"Protocol:\s*(.+?)(?:\n|$)",
        "local_port": r"LocalPort:\s*(.+?)(?:\n|$)",
        "remote_port": r"RemotePort:\s*(.+?)(?:\n|$)",
        "enabled": r"Enabled:\s*(.+?)(?:\n|$)",
    }

    rule = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, block, re.IGNORECASE)
        rule[field] = match.group(1).strip() if match else None

    # Skip if essential fields are missing
    if not all([rule["name"], rule["direction"], rule["action"], rule["protocol"]]):
        return None

    # Parse port information - check both local and remote ports
    port = "Any"
    port_candidates = [rule["local_port"], rule["remote_port"]]

    for port_candidate in port_candidates:
        if port_candidate and port_candidate.lower() != "any":
            port = port_candidate
            break

    # Try to parse as integer if it's a simple number
    if isinstance(port, str) and port.isdigit():
        with contextlib.suppress(ValueError):
            port = int(port)

    # Convert "enabled" field to a boolean
    enabled = rule.get("enabled", "").strip().upper()
    rule["enabled"] = enabled == "YES"

    return {
        "name": rule["name"],
        "direction": rule["direction"].upper(),
        "action": rule["action"].upper(),
        "protocol": rule["protocol"].upper(),
        "enabled": rule["enabled"],
        "port": port,
        "local_port": rule["local_port"],
        "remote_port": rule["remote_port"],
    }


def get_firewall_info(
    ports=None, direction=None, enabled_only=False, exclude_any_ports=False
) -> dict:
    """Return a dict of firewall info."""
    return {
        "enabled": check_firewall_status(),
        "status": "ON" if check_firewall_status() else "OFF",
        "rules": get_firewall_rules(
            ports=ports,
            direction=direction,
            enabled_only=enabled_only,
            exclude_any_ports=exclude_any_ports,
        ),
    }
