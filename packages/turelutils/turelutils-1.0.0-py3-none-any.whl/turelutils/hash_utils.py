import hashlib
from typing import Union
from uuid import UUID, uuid4

def hash_sha256(data: Union[str, bytes]) -> str:
    """Generate a SHA-256 hash from the given data.

    Args:
        data: The data to hash, either as a string or bytes.

    Returns:
        The hexadecimal representation of the SHA-256 hash.
    """
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()

def hash_md5(data: Union[str, bytes]) -> str:
    """Generate an MD5 hash from the given data.

    Args:
        data: The data to hash, either as a string or bytes.

    Returns:
        The hexadecimal representation of the MD5 hash.
    """
    if isinstance(data, str):
        data = data.encode()
    return hashlib.md5(data).hexdigest()

def verify_md5_hash(data: Union[str, bytes], expected_hash: str) -> bool:
    """Verify that the given data matches the expected MD5 hash.

    Args:
        data: The data to verify, either as a string or bytes.
        expected_hash: The expected MD5 hash value in hexadecimal format.

    Returns:
        True if the calculated hash matches the expected hash, False otherwise.

    Raises:
        TypeError: If data is neither a string nor bytes.
    """
    if isinstance(data, str):
        bytes_data = data.encode('utf-8')
    elif isinstance(data, bytes):
        bytes_data = data
    else:
        raise TypeError("Input 'data' must be a string or bytes object.")

    calculated_hash = hashlib.md5(bytes_data).hexdigest()
    return calculated_hash == expected_hash

def generate_uuid() -> UUID:
    """Generate a random UUID (version 4).

    Returns:
        A randomly generated UUID object.
    """
    return uuid4()
