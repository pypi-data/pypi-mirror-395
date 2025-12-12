"""
Mock infrastructure module for IoC Data SDK
Provides base classes and utilities for repository implementations
"""

from .repository.single_repo_base import SingleRepoBase
from .repository.multi_repo_base import MultiRepoBase

__all__ = [
    "SingleRepoBase",
    "MultiRepoBase"
]