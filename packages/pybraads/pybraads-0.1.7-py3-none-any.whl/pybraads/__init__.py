__version__ = "0.1.7"

def version()->str:
    """Return the version of the lib

    Parameters
    ----------
    
    Returns
    -------
    str
        The string with version
    """
    return __version__

# ads functions
from .adsodbc import AdsConnection, AdsQuery

__all__ = [version, AdsConnection, AdsQuery]