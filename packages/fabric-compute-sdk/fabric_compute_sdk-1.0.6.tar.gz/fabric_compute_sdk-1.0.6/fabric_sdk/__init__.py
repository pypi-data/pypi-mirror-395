"""
Fabric SDK - Official Python SDK for Fabric Distributed AI Compute

Submit AI workloads to the Fabric network programmatically.
"""

from .client import FabricClient
from .exceptions import (
    FabricError,
    AuthenticationError,
    JobSubmissionError,
    InsufficientCreditsError,
    JobTimeoutError,
    NetworkError
)
from .types import Job, Node, CreditBalance, JobResult

__version__ = "1.0.6"
__all__ = [
    "FabricClient",
    "FabricError",
    "AuthenticationError",
    "JobSubmissionError",
    "InsufficientCreditsError",
    "JobTimeoutError",
    "NetworkError",
    "Job",
    "Node",
    "CreditBalance",
    "JobResult"
]


