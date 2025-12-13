"""
Coze Workload Identity SDK for Python

A Python SDK for Coze workload identity authentication using OAuth2.0 token exchange.
"""

from .client import Client
from .exceptions import WorkloadIdentityError, TokenExchangeError, ConfigurationError, TokenRetrievalError
from . import env_keys
from .models import ProjectEnvVar, ProjectEnvVars

__version__ = "0.1.1"
__all__ = [
    "Client",
    "WorkloadIdentityError",
    "TokenExchangeError",
    "ConfigurationError",
    "TokenRetrievalError",
    "env_keys",
    "ProjectEnvVar",
    "ProjectEnvVars"
]