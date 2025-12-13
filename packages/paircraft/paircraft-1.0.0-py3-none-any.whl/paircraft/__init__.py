"""
Paircraft - Chess Tournament API SDK

A Python library for interacting with the Paircraft API.
"""

from .client import ChessTournamentClient
from .exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
)
from .models import (
    Tournament,
    Player,
    Pairing,
    Standing,
    Prize,
    Section,
)

__version__ = "1.0.0"
__author__ = "Chess Tournament Director"

__all__ = [
    # Main client
    "ChessTournamentClient",
    
    # Exceptions
    "APIError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    
    # Models
    "Tournament",
    "Player",
    "Pairing",
    "Standing",
    "Prize",
    "Section",
]
