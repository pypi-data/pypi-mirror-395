from datetime import date, datetime
from typing import Any, Optional


def validate_project_name(name: str) -> str:
    """Validate project name for filesystem compatibility.

    Prevents common mistakes while allowing Unicode characters.
    Platform-specific restrictions are handled by the filesystem.

    Args:
        name (str): The project name to validate.

    Returns:
        str: The validated project name.

    Raises:
        ValueError: If the project name is invalid.
    """
    if not name:
        raise ValueError("Project name cannot be empty")

    if name.startswith(("-", ".")):
        raise ValueError("Project name cannot start with '-' or '.'")

    if ".." in name:
        raise ValueError("Project name cannot contain '..'")

    if "/" in name or "\\" in name:
        raise ValueError("Project name cannot contain path separators")

    if len(name) > 255:
        raise ValueError("Project name too long (max 255 characters)")

    return name


def mandatory_datetime(input: Any) -> datetime:
    """Validate an input date and convert it to a datetime object.

    Args:
        input (Any): The input date to validate.

    Returns:
        Optional[datetime]: The validated datetime object or None if the input
            is an empty string.
    """
    if not isinstance(input, date):
        raise ValueError(f"Invalid date format: {input}")

    return datetime.combine(input, datetime.min.time())


def optional_datetime(input: Any) -> Optional[datetime]:
    """Validate an input date and convert it to a datetime object.

    Args:
        input (Any): The input date to validate.

    Returns:
        Optional[datetime]: The validated datetime object or None if the input
            is an empty string.
    """
    if not input:
        return None

    return mandatory_datetime(input)
