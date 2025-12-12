from typing import Any

def take_input(prompt: str, expected_type: type) -> Any:
    user_input = input(prompt)
    try:
        converted_input = expected_type(user_input)
    except ValueError:
        raise ValueError(f"Input could not be converted to {expected_type.__name__}")

    return converted_input