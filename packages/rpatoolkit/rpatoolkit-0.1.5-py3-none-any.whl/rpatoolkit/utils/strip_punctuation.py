import re


def strip_punctuation(text: str, replacement: str = "") -> str:
    """
    Strips  punctuations from a string

    Args:
        text (str): The input string (typically a column header name)
        replacement (str, optional): Character to replace punctuation with. Defaults to '' (removes punctuation).

    Returns:
        str: String with punctuation stripped or replaced

    Examples:
        >>> _strip_punctuation("First Name!")
        'First Name'
        >>> _strip_punctuation("Last, Name")
        'Last Name'
        >>> _strip_punctuation("Age?", replacement='_')
        'Age_'
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    cleaned_text = re.sub(r"[^\w\s]", replacement, text)
    return cleaned_text.strip()
