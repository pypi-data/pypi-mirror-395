from .core import DistribAPI, ResourceType, Endpoint
from .version import __version__

__all__ = ['DistribAPI', 'ResourceType', 'Endpoint', '__version__']

# For easier usage
distrib = DistribAPI()
