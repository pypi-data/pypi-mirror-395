"""Package-level setup information."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

from dkist_processing_core.resource_queue import ResourceQueue
from dkist_processing_core.task import TaskBase
from dkist_processing_core.workflow import Workflow

try:
    __version__ = version(distribution_name=__name__)
except PackageNotFoundError:
    # package is not installed
    __version__ = "unknown"
