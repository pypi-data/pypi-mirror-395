import importlib.metadata

try:
    __version__ = importlib.metadata.version('postcode-eu-ai-tools')
except importlib.metadata.PackageNotFoundError:
    # Fallback for development installs or when package isn't installed
    __version__ = 'unknown'

from .tools import PostcodeEuTools

__all__ = [
    'PostcodeEuTools',
]
