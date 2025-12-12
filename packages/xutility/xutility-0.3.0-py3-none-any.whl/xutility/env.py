import os


def get_env(keys: list[str], default: str | None = None) -> str | None:
    """Get a environment variable by a list of possible keys"""
    for k in keys:
        if v := os.getenv(k):
            return v
    return default
