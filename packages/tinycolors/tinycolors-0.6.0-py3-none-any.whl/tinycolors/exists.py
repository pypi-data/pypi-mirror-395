from typing import Any

def exists(data: Any) -> bool:
    """
    Determine whether a value "exists" according to custom rules.

    Rules:
    - Numbers (int, float) always exist, even if zero.
    - Non-empty strings, lists, and dictionaries exist; empty ones do not.
    - True exists; False does not.
    - None does not exist.

    Args:
        data (Any): The value to check.

    Returns:
        bool: True if the value exists, False otherwise.

    Examples:
        >>> exists(0)
        True
        >>> exists("")
        False
        >>> exists(False)
        False
        >>> exists([1, 2])
        True
    """
    if data is None:
        return False
    if isinstance(data, (str, list, dict)) and len(data) == 0:
        return False
    if isinstance(data, bool):
        return data
    return True


if __name__ == "__main__":
    print(f"exist: {exists(0)}")
    print(f"exist: {exists(0.0)}")
    print(f"does not exist: {exists('')}")
    print(f"does not exist: {exists(None)}")
    print(f"does not exist: {exists([])}")
    print(f"does not exist: {exists({})}")
    print(f"exist: {exists(True)}")
    print(f"does not exist: {exists(False)}")
    print(f"exist: {exists([1, 2])}")