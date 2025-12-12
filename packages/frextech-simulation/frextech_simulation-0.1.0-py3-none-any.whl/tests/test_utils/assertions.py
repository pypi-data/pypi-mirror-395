def assert_dicts_equal(d1: dict, d2: dict) -> None:
    """Assert that two dictionaries are equal."""
    assert d1 == d2, f"Mismatch: {d1} != {d2}"

def assert_in_range(value: float, min_val: float, max_val: float) -> None:
    """Assert that a value is within a specified range."""
    assert min_val <= value <= max_val, f"{value} not in range [{min_val}, {max_val}]"

def assert_keys_present(d: dict, keys: list) -> None:
    """Assert that all specified keys are present in a dictionary."""
    missing = [k for k in keys if k not in d]
    assert not missing, f"Missing keys: {missing}"

def assert_positive(value: float) -> None:
    """Assert that a value is positive."""
    assert value > 0, f"Expected positive value, got {value}"