def bytes_to_mb(b, decimals=1):
    """Megabyte (MB)"""
    return round((b * 8) / (8 * 1000 * 1000), decimals)


def bytes_to_mib(b, decimals=1):
    """Mebibyte (MiB)"""
    return round((b * 8) / (8 * 1024 * 1024), decimals)


def bytes_to_gb(b, decimals=1):
    """Gigabyte (GB)"""
    return round((b * 8) / (8 * 1000 * 1000 * 1000), decimals)


def bytes_to_gib(b, decimals=1):
    """Gibibyte (GiB)"""
    return round((b * 8) / (8 * 1024 * 1024 * 1024), decimals)


def human_readable_bytes(b, metric: bool = True):
    """Convert bytes to a human readable string.
    If you're dealing with data storage or network speeds, you should probably
    use 1000 (metric). If you're dealing with RAM sizes, you should probably
    use 1024."""
    step = 1000 if metric else 1024
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    unit = 0
    while b >= step and unit < len(units) - 1:
        b /= step
        unit += 1
    return f"{round(b, 2)} {units[unit]}"
