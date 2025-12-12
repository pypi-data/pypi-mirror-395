
def milliseconds_to_readable(milliseconds, wrap=True) -> str:
    seconds = int(milliseconds / 1000) % 60
    minutes = int(milliseconds / (1000 * 60)) % 60
    hours = int(milliseconds / (1000 * 60 * 60)) % 24
    ms = milliseconds % 1000

    time = None
    if hours > 0:
        time = f"{hours}h {minutes}m {seconds}s {ms}ms"
    elif minutes > 0:
        time = f"{minutes}m {seconds}s {ms}ms"
    elif seconds > 0:
        time = f"{seconds}s {ms}ms"
    elif ms > 0:
        time = f"{ms}ms"

    if time is not None:
        return f"[{time}]" if wrap else f"{time}"

    return ""
