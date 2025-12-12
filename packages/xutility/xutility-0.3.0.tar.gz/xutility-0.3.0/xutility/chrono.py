import time


def current_sec() -> int:
    return int(time.time())


def current_ms() -> int:
    return int(time.time() * 1_000)


def current_us() -> int:
    return int(time.time() * 1_000_000)
