import secrets
import string


def random_string(
    length: int = 12, characters: str = string.ascii_letters + string.digits
) -> str:
    """
    Generates a random string of the specified length and characters.

    Args:
        length (int, optional): Length of the random string. Defaults to 12.
        characters (str, optional): Characters to use in the random string. Defaults to string.ascii_letters + string.digits.

    Returns:
        str: The generated random string.

    Example:
        >>> random_string(length=10, characters="abcdefghijklmnopqrstuvwxyz")
        'qpoiejmnza'
    """
    return "".join(secrets.choice(characters) for i in range(length))
