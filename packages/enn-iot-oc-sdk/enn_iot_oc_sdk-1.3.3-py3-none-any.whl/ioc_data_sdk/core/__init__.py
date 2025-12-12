"""
Mock core module for IoC Data SDK
Provides fake authentication and business context functionality
"""

from dataclasses import dataclass
from typing import Optional
import threading

# Global thread-local storage for context
_thread_local = threading.local()

@dataclass
class BizContext:
    """
    Mock Business Context for simulating SDK behavior
    """
    eo_id: str = ""
    instance_id: str = ""
    task_id: str = ""
    job_id: str = ""

    def __post_init__(self):
        # Convert all to strings for consistency
        self.eo_id = str(self.eo_id) if self.eo_id else ""
        self.instance_id = str(self.instance_id) if self.instance_id else ""
        self.task_id = str(self.task_id) if self.task_id else ""
        self.job_id = str(self.job_id) if self.job_id else ""

def set_token(auth_token: str, csrf_token: str) -> None:
    """
    Mock function to set authentication tokens
    In real implementation, this would validate tokens with backend
    """
    if not auth_token:
        raise ValueError("auth_token cannot be empty")
    if not csrf_token:
        raise ValueError("csrf_token cannot be empty")

    # Store in thread-local for mock behavior
    _thread_local.auth_token = auth_token
    _thread_local.csrf_token = csrf_token

    print(f"[MOCK] Authentication set - auth_token: {auth_token[:10]}..., csrf_token: {csrf_token[:10]}...")

def set_biz(context: BizContext) -> None:
    """
    Mock function to set business context
    """
    if not isinstance(context, BizContext):
        raise ValueError("context must be a BizContext instance")

    # Store in thread-local for mock behavior
    _thread_local.biz_context = context

    print(f"[MOCK] Business context set - eo_id: {context.eo_id}, instance_id: {context.instance_id}")

def get_current_context() -> Optional[BizContext]:
    """
    Helper function to get current business context
    """
    return getattr(_thread_local, 'biz_context', None)

def get_current_token() -> Optional[dict]:
    """
    Helper function to get current authentication info
    """
    if hasattr(_thread_local, 'auth_token'):
        return {
            'auth_token': _thread_local.auth_token,
            'csrf_token': _thread_local.csrf_token
        }
    return None