import importlib.metadata

from arraylake.client import AsyncClient, Client
from arraylake.config import config
from arraylake.exceptions import (
    ArraylakeClientError,
    ArraylakeHttpError,
    ArraylakeServerError,
    ArraylakeValidationError,
)

__version__ = importlib.metadata.version("arraylake")


__all__ = [
    "__version__",
    "AsyncClient",
    "Client",
    "config",
    "repo",
    "ArraylakeHttpError",
    "ArraylakeClientError",
    "ArraylakeServerError",
    "ArraylakeValidationError",
]
