import re
from typing import Any

NAME_PATTERN = r"^[a-z0-9._-]+$"


def _is_resource_name_correct(resource_name: Any) -> bool:
    """Checks if the given resource name is correct.

    Args:
        resource_name: The resource name to check.

    Returns:
        Whether the resource name is correct.
    """
    return isinstance(resource_name, str) and bool(
        re.match(NAME_PATTERN, resource_name)
    )
