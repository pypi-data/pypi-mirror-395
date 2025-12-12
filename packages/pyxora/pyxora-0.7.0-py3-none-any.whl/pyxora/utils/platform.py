import sys

__all__ = [
    "get_platform","get_web_platform",
    "is_web","is_local",
    "is_windows","is_linux","is_mac","is_android"
]

def get_platform() -> str:
    """
    Get the platform string from the system.

    Returns:
        str: The platform (e.g., 'win32', 'linux', 'darwin', 'emscripten').
    """
    return sys.platform


def is_windows() -> bool:
    """
    Check if the current platform is Windows.

    Returns:
        bool: True if on Windows.
    """
    return get_platform().startswith("win")


def is_linux() -> bool:
    """
    Check if the current platform is Linux.

    Returns:
        bool: True if on Linux.
    """
    return get_platform().startswith("linux")


def is_mac() -> bool:
    """
    Check if the current platform is macOS.

    Returns:
        bool: True if on macOS.
    """
    return get_platform().startswith("darwin")


def is_android() -> bool:
    """
    Check if the current platform is Android.

    Returns:
        bool: True if on Android.
    """
    return hasattr(sys, "getandroidapilevel")


def is_local() -> bool:
    """
    Check if the current platform is a local/native one (not web).

    Returns:
        bool: True if running on Windows, Linux, macOS, or Android.
    """
    return is_windows() or is_linux() or is_mac() or is_android()


def is_web() -> bool:
    """
    Check if the game is running in a web environment (Emscripten).

    Returns:
        bool: True if compiled with Emscripten and running in a browser.
    """
    return get_platform() == "emscripten"


def get_web_platform() -> str | None:
    """
    Attempt to determine the user's OS/platform from the browser user agent.

    Only works if running in a web context (via Emscripten). Parses
    the JavaScript `navigator.userAgent`.

    Returns:
        str | None: One of ['ios', 'android', 'win', 'mac', 'linux', 'unknown'], or None if not in web.
    """
    if not is_web():
        return None

    # Import JavaScript interop module available in Pyodide/Emscripten
    user_agent = __import__("js").navigator.userAgent.lower()
    web_platforms = {
        "iphone": "ios",
        "ipad": "ios",
        "android": "android",
        "windows": "win",
        "macintosh": "mac",
        "linux": "linux"
    }
    return next((v for k, v in web_platforms.items() if k in user_agent), "unknown")
