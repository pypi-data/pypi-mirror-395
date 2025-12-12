"""
Enforce ranges, uniqueness, correlations in generated data
"""


def enforce_range(value, min_val, max_val):
    """Ensure value is within specified range"""
    return max(min_val, min(max_val, value))


def ensure_uniqueness(data_list):
    """Remove duplicates from list while preserving order"""
    seen = set()
    result = []
    for item in data_list:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def apply_correlation(base_value, correlation_factor=0.5):
    """Apply correlation to generate related values"""
    import random
    noise = random.uniform(-0.1, 0.1)
    return base_value * (1 + correlation_factor * noise)
