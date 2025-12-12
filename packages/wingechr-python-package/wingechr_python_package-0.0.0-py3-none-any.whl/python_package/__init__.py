"""MODULE DESCRIPTION"""

import platform
import sys

__version__ = "0.0.0"
__all__ = []


def get_info() -> dict:
    """Return information about the system.

    Returns
    -------
    dict


    Examples
    --------
    >>> sorted(get_info().keys())
    ['platform', 'python', 'version']

    """

    return {
        "platform": platform.system(),
        "python": sys.version.split(" ")[0],
        "version": __version__,
    }
