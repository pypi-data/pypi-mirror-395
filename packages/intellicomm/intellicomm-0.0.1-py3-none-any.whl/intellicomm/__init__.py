"""
IntelliComm Protocol (ICP) - Intelligent Communication Framework

A powerful framework for creating intelligent communication protocols between agents,
servers, and clients with beautiful console output and structured message handling.

Author: Ahsen Tahir
Version: 1.0.0
License: MIT
"""

__version__ = "0.0.1"
__author__ = "Ahsen Tahir"
__email__ = "ahsentahir007@gmail.com"
__license__ = "MIT"

# Import main classes for easy access
from .server import Server
from .client import Client
from .http_server import HttpServer
from .http_client import HttpClient
from .payments import PaymentConfig, load_wallet_config, get_payment_address

# Define what gets imported with "from intellicomm import *"
__all__ = [
    "Server",
    "Client",
    "HttpServer",
    "HttpClient",
    "PaymentConfig",
    "load_wallet_config",
    "get_payment_address",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "get_version",
    "get_info"
]

# Package initialization
def get_version():
    """Get the current version of IntelliComm Protocol."""
    return __version__

def get_info():
    """Get package information."""
    return {
        "name": "IntelliComm Protocol",
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "license": __license__,
        "description": "Intelligent Communication Framework for agents via servers and clients"
    }

# Initialize package-level logging or configuration here if needed
def _initialize_package():
    """Initialize package-level settings."""
    # This runs when the package is imported
    pass

# Run initialization
_initialize_package()
