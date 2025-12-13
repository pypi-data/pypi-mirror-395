import platform


def get_system_info() -> str:
    os_name = platform.system()  # e.g., "Darwin", "Windows", "Linux"
    os_version = platform.version()  # e.g., "19.6.0", "10.0.19043", "5.15.0-84-generic"
    python_version = platform.python_version()  # Python version

    return f"{detect_operating_system(os_name)}; {os_name} {os_version}; Python{python_version}"


def detect_operating_system(raw_input: str) -> str:
    if raw_input is None:
        return "Unknown"

    os_name = raw_input.lower()
    if "darwin" in os_name:
        return "Macintosh"
    elif "win" in os_name:
        return "Windows"
    elif "linux" in os_name:
        return "Linux"
    else:
        return "Other"
