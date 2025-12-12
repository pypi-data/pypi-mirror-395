def clean_name(name: str) -> str:
    """Return a clean processor name."""
    name = name.replace("(R)", "").replace("(TM)", "")
    return name.split("CPU @")[0].strip()
