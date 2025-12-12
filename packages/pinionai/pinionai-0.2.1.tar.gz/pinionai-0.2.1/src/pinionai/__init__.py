# pinionai/__init__.py

"""
PinionAI Python Client

This is the official Python client library for the PinionAI platform.
"""

__version__ = "1.0.0"  # Version of the package
from .client import AsyncPinionAIClient
from .client import format_phone, twilio_sms_message
from .chatservice_pb2_grpc import ChatServiceStub
from .exceptions import (
    PinionAIAPIError,
    PinionAIConfigurationError,
    PinionAIGrpcError,
    PinionAIError,
    PinionAISessionError,
)

__all__ = [
    "AsyncPinionAIClient",
    "format_phone",
    "twilio_sms_message",
    "PinionAIError",
    "PinionAIConfigurationError",
    "PinionAIAPIError",
    "PinionAISessionError",
    "PinionAIGrpcError",
    "ChatServiceStub",
]