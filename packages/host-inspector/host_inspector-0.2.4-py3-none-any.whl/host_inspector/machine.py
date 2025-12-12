import uuid
from functools import cache

import machineid


@cache
def get_machine_id() -> str:
    """Return consistent UUID format."""
    string = machineid.id().strip()
    return str(uuid.UUID(string))
