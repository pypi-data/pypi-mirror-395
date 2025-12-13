"""Type definitions for Fabric SDK"""

from typing import TypedDict, Optional, Dict, Any, Literal
from datetime import datetime


JobStatus = Literal["queued", "executing", "completed", "failed"]
NodeStatus = Literal["active", "inactive", "busy", "removed"]


class Job(TypedDict, total=False):
    """Job representation - matches backend JobResponse model"""
    id: str
    job_type: str
    status: JobStatus
    assigned_node_id: Optional[str]
    estimated_cost: Optional[float]
    actual_cost: Optional[float]
    queued_at: str
    started_at: Optional[str]
    completed_at: Optional[str]
    duration_seconds: Optional[float]
    timeout_at: Optional[str]
    warning: Optional[Dict[str, Any]]


class Node(TypedDict, total=False):
    """Node representation - matches backend /api/nodes response"""
    id: str
    device_id: str
    name: str
    status: NodeStatus
    hardware_info: Dict[str, Any]
    gpu_info: Optional[Dict[str, Any]]
    jobs_completed: int
    lifetime_earnings: float
    current_balance: float
    enrolled_at: str
    last_heartbeat: Optional[str]


class CreditBalance(TypedDict, total=False):
    """Credit balance representation - matches backend /api/payment/balance response"""
    user_id: str
    credits_balance: float  # Access with balance['credits_balance']
    pending_earnings: float
    lifetime_earnings: float
    lifetime_spending: float


class JobResult(TypedDict):
    """Job result with metadata"""
    job_id: str
    status: JobStatus
    result: Optional[Dict[str, Any]]
    actual_cost: float
    duration_seconds: Optional[float]
    error_message: Optional[str]

