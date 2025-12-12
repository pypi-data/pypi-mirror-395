import logging
import subprocess

logger = logging.getLogger(__name__)


def port_to_name(port: str) -> str:
    """Return a friendly name for a port or comma-separated ports.
    If multiple ports map to the same name, only include the label once.
    """
    port_map = {
        "80": "HTTP",
        "443": "HTTPS",
        "22": "SSH",
        "1883": "MQTT",
        "3000": "Node",
        "9001": "MQTT",
        "5432": "PostgreSQL",
        "8000": "HTTP",
        "8080": "HTTP",
        "8883": "MQTT",
    }
    ports = [p.strip() for p in port.split(",")] if port else []
    # Use a set to avoid duplicate names, but preserve order
    seen = set()
    names = []
    for p in ports:
        label = port_map.get(p, p)
        if label not in seen:
            names.append(label)
            seen.add(label)
    return ",".join(names) if names else None


def is_firewall_enabled() -> bool:
    """
    Checks the status of the firewall using common Linux commands.
    Returns a tuple: (status_string, command_used)
    """
    commands = {
        "ufw": "sudo ufw status",
        # "firewalld": "sudo firewall-cmd --state",
        # "iptables": "sudo iptables -L -n",
    }

    # Check for each firewall manager in a preferred order
    for command in commands.values():
        try:
            # We use `shell=True` for simplicity, but for security,
            # it's better to pass a list of arguments for user-provided input.
            process = subprocess.run(  # noqa: S602
                command, shell=True, capture_output=True, text=True, check=True
            )
            output = process.stdout.strip().lower()

            if "inactive" in output:
                return False
            return bool("active" in output or "running" in output)

        except subprocess.CalledProcessError:
            # The command failed, likely because the manager is not installed
            # or not running. We can ignore this and try the next one.
            pass
        except FileNotFoundError:
            # The command itself was not found.
            pass

    # If none of the commands worked
    return False


def get_firewall_rules(
    ports=None, direction=None, enabled_only=False, exclude_any_ports=False
):
    command = ["sudo", "ufw", "status", "verbose"]

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
        logger.warning("Error executing command %s", command)
        return []


def parse_firewall_output(
    output, ports_filter=None, enabled_only=False, exclude_any_ports=False
):
    lines = output.strip().split("\n")
    rules = []

    # Find the line that marks the beginning of the rules table
    start_index = -1
    for i, line in enumerate(lines):
        if "To" in line and "Action" in line and "From" in line:
            start_index = i + 2  # Skip the header line and separator line
            break

    if start_index == -1:
        return rules  # No rules found or output format is different

    rule_lines = lines[start_index:]

    for line in rule_lines:
        line = line.strip()  # noqa: PLW2901
        if not line or line.startswith("--"):  # Skip empty lines and separator lines
            continue
        if "(v6)" in line:  # Skip IPv6 rules for simplicity
            continue

        # Split the line into parts, but be careful with whitespace
        parts = line.split()
        if len(parts) < 3:  # noqa: PLR2004
            continue

        # The format is: To | Action | From
        # Example: "22/tcp                     ALLOW IN    Anywhere"
        #          "1883,9001/tcp              ALLOW IN    Anywhere"
        to_part = parts[0]
        action_part = parts[1]  # This is "ALLOW" or "DENY"
        direction_part = parts[2] if len(parts) > 2 else "IN"  # noqa: PLR2004
        from_part = parts[3] if len(parts) > 3 else "ANY"  # noqa: PLR2004

        # Parse the "To" field which contains port/protocol
        protocol = "ANY"
        port = None

        if "/" in to_part:
            port_proto = to_part.split("/")
            port_part = port_proto[0]  # Could be "22" or "1883,9001"
            protocol = port_proto[1].upper()
            port = port_part  # Keep comma-separated ports as-is
        else:
            # Handle cases where there's no protocol specified
            port = to_part if to_part else None

        # Standardize action and direction
        action = "ALLOW" if "ALLOW" in action_part.upper() else "DENY"
        direction = (
            "INBOUND" if "IN" in direction_part or "OUT" not in line else "OUTBOUND"
        )

        from_port = "ANY" if from_part == "Anywhere" else from_part

        # Create single rule
        rule = {
            "name": port_to_name(port) if port else None,
            "direction": direction,
            "action": action,
            "protocol": protocol,
            "enabled": True,
            "local_port": port,
            "remote_port": from_port,
        }
        rules.append(rule)

    return rules


def get_firewall_info(
    ports=None,
    direction=None,
    enabled_only=False,
    exclude_any_ports=False,
) -> dict:
    """Return a dict of firewall info."""
    enabled = is_firewall_enabled()
    return {
        "enabled": enabled,
        "status": "ON" if enabled else "OFF",
        "rules": get_firewall_rules(
            ports=ports,
            direction=direction,
            enabled_only=enabled_only,
            exclude_any_ports=exclude_any_ports,
        ),
    }
