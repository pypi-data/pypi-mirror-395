"""
Fabric SDK - Official Python SDK for Fabric Distributed AI Compute

Submit AI workloads to the Fabric network programmatically.

Copyright 2025 Carmel Labs, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
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

__version__ = "1.0.8"
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


