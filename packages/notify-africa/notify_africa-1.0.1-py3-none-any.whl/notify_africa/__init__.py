"""
Notify Africa SMS SDK

A Python SDK for integrating with Notify Africa SMS service.
"""

__version__ = "1.0.0"
__author__ = "Notify Africa"
__email__ = "support@notifyafrica.com"

from .client import NotifyAfrica
from .models import (
    SendSingleRequest,
    SendSingleResponse,
    SendBatchRequest,
    SendBatchResponse,
    MessageStatusResponse
)
from .exceptions import (
    NotifyAfricaException,
    AuthenticationError,
    ValidationError,
    InsufficientCreditsError,
    NetworkError
)

__all__ = [
    'NotifyAfrica',
    'SendSingleRequest',
    'SendSingleResponse',
    'SendBatchRequest',
    'SendBatchResponse',
    'MessageStatusResponse',
    'NotifyAfricaException',
    'AuthenticationError',
    'ValidationError',
    'InsufficientCreditsError',
    'NetworkError'
]