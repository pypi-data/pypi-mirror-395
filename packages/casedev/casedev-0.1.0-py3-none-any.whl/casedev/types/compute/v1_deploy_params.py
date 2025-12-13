# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._types import SequenceNotStr
from ..._utils import PropertyInfo

__all__ = ["V1DeployParams", "Config"]


class V1DeployParams(TypedDict, total=False):
    entrypoint_name: Required[Annotated[str, PropertyInfo(alias="entrypointName")]]
    """Function/app name (used for domain: hello → hello.org.case.systems)"""

    type: Required[Literal["task", "service"]]
    """Deployment type: task for batch jobs, service for web endpoints"""

    code: str
    """Python code (required for python runtime)"""

    config: Config
    """Runtime and resource configuration"""

    dockerfile: str
    """Dockerfile content (required for dockerfile runtime)"""

    entrypoint_file: Annotated[str, PropertyInfo(alias="entrypointFile")]
    """Python entrypoint file name"""

    environment: str
    """Environment name (uses default if not specified)"""

    image: str
    """
    Container image name (required for image runtime, e.g.,
    'nvidia/cuda:12.8.1-devel-ubuntu22.04')
    """

    runtime: Literal["python", "dockerfile", "image"]
    """Runtime environment"""


class Config(TypedDict, total=False):
    add_python: Annotated[str, PropertyInfo(alias="addPython")]
    """Add Python to image (e.g., '3.12', for image runtime)"""

    allow_network: Annotated[bool, PropertyInfo(alias="allowNetwork")]
    """Allow network access (default: false for Python, true for Docker)"""

    cmd: SequenceNotStr[str]
    """Container command arguments"""

    concurrency: int
    """Concurrent execution limit"""

    cpu_count: Annotated[int, PropertyInfo(alias="cpuCount")]
    """CPU core count"""

    cron_schedule: Annotated[str, PropertyInfo(alias="cronSchedule")]
    """Cron schedule for periodic execution"""

    dependencies: SequenceNotStr[str]
    """Python package dependencies (python runtime)"""

    entrypoint: SequenceNotStr[str]
    """Container entrypoint command"""

    env: Dict[str, str]
    """Environment variables"""

    gpu_count: Annotated[int, PropertyInfo(alias="gpuCount")]
    """Number of GPUs (for multi-GPU setups)"""

    gpu_type: Annotated[
        Literal["cpu", "T4", "L4", "A10G", "L40S", "A100", "A100-40GB", "A100-80GB", "H100", "H200", "B200"],
        PropertyInfo(alias="gpuType"),
    ]
    """GPU type for acceleration"""

    is_web_service: Annotated[bool, PropertyInfo(alias="isWebService")]
    """Deploy as web service (auto-set for service type)"""

    memory_mb: Annotated[int, PropertyInfo(alias="memoryMb")]
    """Memory allocation in MB"""

    pip_install: Annotated[SequenceNotStr[str], PropertyInfo(alias="pipInstall")]
    """Packages to pip install (image runtime)"""

    port: int
    """Port for web services"""

    python_version: Annotated[str, PropertyInfo(alias="pythonVersion")]
    """Python version (e.g., '3.11')"""

    retries: int
    """Retry attempts on failure (Python only)"""

    secret_groups: Annotated[SequenceNotStr[str], PropertyInfo(alias="secretGroups")]
    """Secret group names to inject"""

    timeout_seconds: Annotated[int, PropertyInfo(alias="timeoutSeconds")]
    """Maximum execution time"""

    use_uv: Annotated[bool, PropertyInfo(alias="useUv")]
    """Use uv for faster package installs"""

    warm_instances: Annotated[int, PropertyInfo(alias="warmInstances")]
    """Number of warm instances to maintain"""

    workdir: str
    """Working directory in container"""
