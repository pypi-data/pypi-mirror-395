import re


def validate_type(value, name, expected_type):
    if not isinstance(value, expected_type):
        raise TypeError(f"Parameter '{name}' must be of type {expected_type.__name__}, got {type(value).__name__}.")


def validate_range(value, name, min_val=None, max_val=None):
    if min_val is not None and value < min_val:
        raise ValueError(f"Parameter '{name}' must be greater than or equal to {min_val}, got {value}.")
    if max_val is not None and value > max_val:
        raise ValueError(f"Parameter '{name}' must be less than or equal to {max_val}, got {value}.")


def validate_string_choice(value, name, choices):
    if value.lower() not in choices:
        raise ValueError(f"Invalid value for '{name}'. Must be one of {choices}, got '{value}'.")


def validate_locator(locator):
    if not isinstance(locator, str) or not locator.strip():
        raise TypeError("The 'locator' must be a non-empty string.")
    if '=' not in locator:
        raise ValueError(f"Locator '{locator}' must be in the format 'strategy=value'.")
    strategy, value = locator.split('=', 1)
    if strategy.strip() != strategy or value.strip() != value:
        raise ValueError(f"Locator '{locator}' must not contain spaces around '='.")


def validate_android_package_name(package_name):
    """Valida se o nome do pacote segue as convenções do Android."""
    if not package_name or not isinstance(package_name, str):
        return False
    # Padrão regex para nomes de pacotes Android
    android_package_pattern = r'^[a-zA-Z][a-zA-Z0-9_-]*(\.[a-zA-Z][a-zA-Z0-9_-]*)+$'
    return bool(re.match(android_package_pattern, package_name))