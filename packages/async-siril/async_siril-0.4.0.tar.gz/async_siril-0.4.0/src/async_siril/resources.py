from __future__ import annotations
import typing as t

from dataclasses import dataclass
from .system import container_aware_cpu_limit, container_aware_memory_limit_gb


@dataclass
class SirilResource:
    """Represents the resources to use for Siril"""

    # How much CPU to use (in number of cores, default is all)
    cpu_limit: t.Optional[int] = None

    # How much memory to use (in GB, default is 90% of available memory)
    memory_limit: t.Optional[str] = None

    # How much of the available memory to use (0.9 = 90%, default is 90%)
    memory_percent: float = 0.9

    @staticmethod
    def container_aware_limits() -> SirilResource:
        """Get the limits for Siril in a container environment"""
        return SirilResource(
            cpu_limit=container_aware_cpu_limit(),
            memory_limit=container_aware_memory_limit_gb(),
        )

    @staticmethod
    def default_limits() -> SirilResource:
        """Get the default limits for Siril"""
        return SirilResource()
