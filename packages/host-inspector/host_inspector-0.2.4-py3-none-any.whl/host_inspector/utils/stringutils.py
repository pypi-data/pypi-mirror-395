import re


def formatted_number(number) -> str:
    return f"{number:,}"


def formatted_percentage(number) -> str:
    return f"{number:,.2f}%"


def formatted_date(date) -> str:
    return date.strftime("%A, %B %d, %Y")


def extract_version(string) -> str:
    match = re.search(r"([\d.]+)", string)
    if match:
        return match.group(1)
    return "--"
