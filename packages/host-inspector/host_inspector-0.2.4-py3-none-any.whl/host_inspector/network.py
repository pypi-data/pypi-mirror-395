import platform
import re
import socket
import uuid
from functools import cache

import psutil

# import requests
# from requests.exceptions import RequestException

# Socket constants not the same on all platforms
AF_INET = [2]  # IPv4 (Mac, Linux, Windows)
AF_INET6 = [30, 10, 23]  # IPv6 (Mac, Linux, Windows)
AF_LINK = [18, 17, -1]  # MAC address (Mac, Linux, Windows)


# @cache
# def external_ip() -> str:
#     """Safely return external IP."""
#     try:
#         resp = requests.get("https://api.ipify.org", timeout=5)
#         return resp.text.strip()
#     except RequestException:  # pragma: no cover
#         return "--"


def ip_address() -> str:
    """Safely get internal IP."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:  # pragma: no cover
        return "--"


def get_node_as_mac_address() -> str:
    """Not full-proof, but should get the job done."""
    return ":".join(re.findall("..", f"{uuid.getnode():012x}"))


@cache
def get_network_interface_by_ip(ip) -> tuple:
    """Return the network interface by IP."""
    intfaces = psutil.net_if_addrs()
    for name in intfaces:
        for nicaddress in intfaces[name]:
            if nicaddress.address == ip:
                return name, intfaces[name]
    return "--", []  # pragma: no cover


@cache
def get_mac_address_for_ip(ip) -> str:
    """Return MAC address for network interface by IP."""
    _, addresses = get_network_interface_by_ip(ip)
    mac = next((x.address for x in addresses if x.family in AF_LINK), "")
    return mac.lower().replace("-", ":") if mac else "--"


@cache
def get_ipv6_address_for_ip(ip) -> str:
    """Return IPv6 address for network interface by IP."""
    _, addresses = get_network_interface_by_ip(ip)
    ipv6_address = next((x.address for x in addresses if x.family in AF_INET6), "")
    return ipv6_address.split("%")[0] if ipv6_address else "--"


def get_network_info() -> dict:
    """Return network info as dict."""

    ip = ip_address()
    intface_name, _ = get_network_interface_by_ip(ip)

    return {
        "hostname": platform.node(),
        "ip_address": ip,
        "ipv6_address": get_ipv6_address_for_ip(ip),
        # "external_ip": external_ip(),
        "node_address": get_node_as_mac_address(),
        "mac_address": get_mac_address_for_ip(ip),
        "interface": intface_name,
    }
