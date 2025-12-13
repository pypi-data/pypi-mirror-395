"""Exception classes for Fabric SDK"""


class FabricError(Exception):
    """Base exception for all Fabric SDK errors"""
    pass


class AuthenticationError(FabricError):
    """Raised when authentication fails"""
    pass


class JobSubmissionError(FabricError):
    """Raised when job submission fails"""
    pass


class InsufficientCreditsError(FabricError):
    """Raised when user has insufficient credits"""
    pass


class JobTimeoutError(FabricError):
    """Raised when job execution times out"""
    pass


class NetworkError(FabricError):
    """Raised when network request fails"""
    pass


