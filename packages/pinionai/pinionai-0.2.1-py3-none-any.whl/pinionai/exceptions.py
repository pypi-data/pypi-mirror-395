"""
Custom exceptions for the PinionAIClient library.
"""

class PinionAIError(Exception):
    """Base exception class for PinionAI client errors."""
    def __init__(self, message="An unspecified error occurred with the PinionAI client."):
        self.message = message
        super().__init__(self.message)

class PinionAIConfigurationError(PinionAIError):
    """Raised for errors in client configuration."""
    def __init__(self, message="Client configuration error."):
        super().__init__(message)

class PinionAIAPIError(PinionAIError):
    """Raised for errors when interacting with the PinionAI API."""
    def __init__(self, message="API interaction error.", status_code=None, details=None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details

    def __str__(self):
        return f"{self.message} (Status: {self.status_code}, Details: {self.details})"

class PinionAISessionError(PinionAIError):
    """Raised for errors related to session management."""
    def __init__(self, message="Session management error."):
        super().__init__(message)

class PinionAIGrpcError(PinionAIError):
    """Raised for errors related to gRPC communication."""
    def __init__(self, message="gRPC communication error.", grpc_code=None):
        super().__init__(message)
        self.grpc_code = grpc_code

    def __str__(self):
        return f"{self.message} (gRPC Code: {self.grpc_code})"