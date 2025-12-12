def clean_name(name: str) -> str:
    """Return a clean GPU name."""
    return name.replace("(R)", "").replace("(TM)", "")
