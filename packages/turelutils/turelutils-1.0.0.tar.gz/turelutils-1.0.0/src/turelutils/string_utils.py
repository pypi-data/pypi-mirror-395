import re
import secrets
from constants import ALPHANUMERIC
from typing import Optional

def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug format.

    Args:
        text: The text to slugify.

    Returns:
        A lowercase slug with spaces replaced by hyphens.
    """
    words = text.split()
    words = [x.lower() for x in words]
    words = "-".join(words)
    return words

def camel_to_snake(text: str) -> str:
    """Convert camelCase string to snake_case.

    Args:
        text: A camelCase formatted string.

    Returns:
        The string converted to snake_case.

    Raises:
        ValueError: If the input is not in valid camelCase format.
    """
    if not re.fullmatch(r'[a-z]+(?:[A-Z][a-z0-9]*)*', text):
        raise ValueError(f"Invalid camelCase format: '{text}'")
    words = [x.lower() for x in re.findall(r'[A-Z]?[a-z0-9]+|[A-Z]+(?![a-z])', text)]
    return "_".join(words)

def snake_to_camel(text: str) -> str:
    """Convert snake_case string to camelCase.

    Args:
        text: A snake_case formatted string.

    Returns:
        The string converted to camelCase.
    """
    words = text.split("_")
    return words[0].lower() + "".join([y.lower().capitalize() for y in words[1:]])

def pascal_to_snake(text: str) -> str:
    """Convert PascalCase string to snake_case.

    Args:
        text: A PascalCase formatted string.

    Returns:
        The string converted to snake_case.

    Raises:
        ValueError: If the input is not in valid PascalCase format.
    """
    if not re.fullmatch(r'[A-Z][a-z0-9]*(?:[A-Z][a-z0-9]*)*', text):
        raise ValueError(f"Invalid PascalCase format: '{text}'")
    words = [x.lower() for x in re.findall(r'[A-Z]?[a-z0-9]+|[A-Z]+(?![a-z])', text)]
    return "_".join(words)

def snake_to_pascal(text: str) -> str:
    """Convert snake_case string to PascalCase.

    Args:
        text: A snake_case formatted string.

    Returns:
        The string converted to PascalCase.
    """
    words = text.split("_")
    return "".join([y.lower().capitalize() for y in words])

def truncate(text: str, length: int, suffix: Optional[str]="…") -> str:
    """Truncate text to a maximum length with an optional suffix.

    Args:
        text: The text to truncate.
        length: The maximum length of the text.
        suffix: Optional suffix to append when truncating (default: "…").

    Returns:
        The truncated text with the suffix appended if needed.
    """
    if len(text) <= length:
        return text
    if suffix:
        return text[:length] + suffix
    return text[:length]

def random_string(lenght: int=12, charset: Optional[str]=None) -> str:
    """Generate a cryptographically secure random string.

    Args:
        lenght: The desired length of the random string (default: 12).
        charset: Optional character set to choose from (default: ALPHANUMERIC).

    Returns:
        A random string of the specified length.
    """
    if not charset:
        charset = ALPHANUMERIC
    string = ""
    for _ in range(lenght):
        string += secrets.choice(charset)
    return string

def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from text.

    Args:
        text: The text containing potential ANSI escape sequences.

    Returns:
        The text with all ANSI escape sequences removed.
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)
