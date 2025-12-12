"""
The filesystem module contains several utility functions related to fs
"""

from pathlib import Path
from datetime import datetime, timezone
from rpatoolkit.utils import random_string


def make_unique_dir(
    base_path: str | Path = ".",
    prefix: str | None = "",
    suffix: str | None = None,
    include_date: bool = True,
    include_time: bool = True,
    use_12h_format: bool = True,
    separator: str = "_",
    time_separator: str = ".",
    date_separator: str = ".",
    create: bool = True,
) -> Path:
    """
    Creates a unique directory with an optionally formatted name based on current date/time and UUID.

    The directory name is constructed using the provided parameters in the format:
    {prefix}{separator}{date_part}{separator}{time_part}{separator}{suffix}

    Args:
        base_path (str | Path, optional): The base directory path where the unique directory will be created. Defaults to "." (current directory).
        prefix (str | None, optional): A prefix to add to the directory name. Defaults to "".
        suffix (str | None, optional): A suffix to add to the directory name. Defaults to a a 12 character alphanumeric string.
        include_date (bool, optional): Whether to include the current date in the directory name. Defaults to True.
        include_time (bool, optional): Whether to include the current time in the directory name. Defaults to True.
        use_12h_format (bool, optional): Whether to use 12-hour format for time (with AM/PM). If False, uses 24-hour format. Defaults to True.
        separator (str, optional): The separator to use between different parts of the directory name. Defaults to "_".
        time_separator (str, optional): The separator to use between time components (hour, minute, second). Defaults to ".".
        date_separator (str, optional): The separator to use between date components (day, month, year). Defaults to ".".
        create (bool, optional): Whether to actually create the directory on the filesystem. If False, only returns the path without creating. Defaults to True.

    Returns:
        Path: The Path object of the created (or to-be-created) unique directory.

    Example:
        >>> unique_dir = make_unique_dir(prefix="backup", include_time=False)
        >>> print(unique_dir)
        backup_24.10.24_a2b3c4d5-e6f7-8901-2345-678901234567
    """
    now = datetime.now(timezone.utc)
    if suffix is None:
        suffix = random_string()

    date_part = ""
    if include_date:
        date_part = now.strftime(f"%d{date_separator}%m{date_separator}%y")

    time_part = ""
    if include_time:
        if use_12h_format:
            time_format = f"%I{time_separator}%M{time_separator}%S_%p"
        else:
            time_format = f"%H{time_separator}%M{time_separator}%S"

        time_part = now.strftime(time_format)

    # Collect all non-empty parts
    parts = []
    if prefix:
        parts.append(prefix)
    if date_part:
        parts.append(date_part)
    if time_part:
        parts.append(time_part)
    if suffix:
        parts.append(suffix)

    if not parts:
        return Path(base_path)

    base_name = separator.join(parts)

    full_path = Path(base_path) / base_name

    # Create the directory if it doesn't exist
    if create:
        full_path.mkdir(parents=True, exist_ok=True)

    return full_path
