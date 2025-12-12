"""
Aggregated API client for IvyBloom CLI.
"""

from __future__ import annotations

from .account import AccountClientMixin
from .base import BaseAPIClient
from .config_client import ConfigClientMixin
from .data_files import DataFilesClientMixin
from .exports import ExportsClientMixin
from .jobs import JobsClientMixin
from .projects import ProjectsClientMixin
from .reports import ReportsClientMixin
from .tools import ToolsClientMixin
from .workflows import WorkflowsClientMixin


class IvyBloomAPIClient(
    BaseAPIClient,
    ToolsClientMixin,
    JobsClientMixin,
    ProjectsClientMixin,
    AccountClientMixin,
    WorkflowsClientMixin,
    DataFilesClientMixin,
    ConfigClientMixin,
    ReportsClientMixin,
    ExportsClientMixin,
):
    """HTTP client for ivybloom API."""


__all__ = ["IvyBloomAPIClient"]

