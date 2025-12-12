from pydantic import ValidationError


def errors_on_lines(e: ValidationError) -> str:
    lines = list({d_e.get("loc", "unknown")[0] for d_e in e.errors()})
    max_lines = max(lines)
    min_lines = min(lines)
    current_range = range(min_lines, max_lines)
    ranges = []
    for i in lines:
        if i not in current_range and i != max_lines:
            previous_range = range(current_range.start, i)
            ranges.append(previous_range)
            current_range = range(i + 1, max_lines)
    ranges.append(current_range)

    message = ""
    for r in ranges:
        message = message + f"{r.start} to {r.stop}, "
    return message
