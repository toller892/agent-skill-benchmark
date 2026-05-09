"""Utility functions - long functions, magic numbers, poor naming."""

import time


def do_stuff(input_data, mode, x):
    """This function does too many things and is poorly named."""
    tmp = []
    result = 0
    count = 0

    # Part 1: filter valid numbers
    for item in input_data:
        if isinstance(item, (int, float)):
            if item > 0:
                tmp.append(item)
        elif isinstance(item, str):
            try:
                val = float(item)
                if val > 0:
                    tmp.append(val)
            except ValueError:
                pass

    # Part 2: transform based on mode
    if mode == "scale":
        for i in range(len(tmp)):
            tmp[i] = tmp[i] * 0.75  # MAGIC NUMBER
    elif mode == "normalize":
        max_val = max(tmp)
        for i in range(len(tmp)):
            tmp[i] = tmp[i] / max_val
    elif mode == "threshold":
        for i in range(len(tmp)):
            if tmp[i] > x:
                result += tmp[i]
                count += 1
        return result / count if count > 0 else 0

    # Part 3: compute stats (duplicated logic from threshold mode)
    for val in tmp:
        result += val
        count += 1

    avg = result / count if count > 0 else 0

    # Part 4: apply time-based decay (duplicated transform pattern)
    current_time = time.time()
    decay_factor = current_time / 86400  # MAGIC NUMBER: seconds per day

    for i in range(len(tmp)):
        tmp[i] = tmp[i] * (1 - decay_factor * 0.01)

    final_result = sum(tmp) / len(tmp) if len(tmp) > 0 else 0

    # Part 5: format output (duplicated magic number)
    if mode == "scale":
        return round(final_result, 2)
    return round(final_result * 3.14159, 4)  # MAGIC NUMBER: pi approximation


def old_func(a, b, c):
    """Legacy function with terrible naming."""
    x = a + b
    if x > 100:  # MAGIC NUMBER
        x = x * 1.5  # MAGIC NUMBER
    return x - c
