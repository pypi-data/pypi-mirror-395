"""Global test fixtures."""

from contextlib import contextmanager
from pathlib import Path
from shutil import rmtree
from typing import Any
from unittest.mock import MagicMock

import pytest
from talus import DurableProducer

from dkist_processing_core import ResourceQueue
from dkist_processing_core import TaskBase
from dkist_processing_core import Workflow
from dkist_processing_core.node import Node
from dkist_processing_core.node import task_type_hint
from dkist_processing_core.tests.task_example import Task


@pytest.fixture(scope="module")
def export_path() -> str:
    """Export path object that will be removed on teardown."""
    path = Path("export/")
    yield str(path)
    rmtree(path, ignore_errors=True)


@pytest.fixture(scope="session")
def task_subclass():
    """Subclass of the abstract task base class implementing methods that are expected to be subclassed with inspect-able metadata."""
    return Task


@pytest.fixture(scope="session")
def error_task_subclass():
    """Subclass of the abstract task base class implementing methods that are expected to be subclassed with inspect-able metadata."""

    class Task(TaskBase):
        def __init__(self, *args, **kwargs):
            self.run_was_called = False
            self.post_run_was_called = False
            super().__init__(*args, **kwargs)

        def run(self):
            self.run_was_called = True

        def post_run(self) -> None:
            self.post_run_was_called = True
            raise RuntimeError("error recording provenance")

    return Task


@pytest.fixture()
def task_instance(task_subclass):
    """Create an instance of the task subclass defined in task_subclass."""
    with task_subclass(
        recipe_run_id=1, workflow_name="workflow_name", workflow_version="version"
    ) as task:
        yield task


@pytest.fixture()
def workflow():
    """Create an instance of the Workflow abstraction without tasks."""
    input_data = "input"
    output_data = "output"
    category = "instrument"
    detail = "workflow_information"
    version = "V6-12342"
    tags = ["tag1", "tag2"]
    workflow_instance = Workflow(
        input_data=input_data,
        output_data=output_data,
        category=category,
        detail=detail,
        workflow_version=version,
        workflow_package=__package__,
        tags=tags,
    )
    return (
        workflow_instance,
        input_data,
        output_data,
        category,
        detail,
        version,
        tags,
    )


@pytest.fixture()
def workflow_tasks(task_subclass) -> list[task_type_hint]:
    """List of Tasks that can be composed into a workflow."""

    class TaskA(task_subclass):
        pass

    class TaskB(task_subclass):
        pass

    class TaskC(task_subclass):
        pass

    class TaskD(task_subclass):
        pass

    return [TaskA, TaskB, TaskC, TaskD]


@pytest.fixture(params=["default", "non_default"])
def queue_name(request):
    """Name of the queue on the Node"""
    if request.param == "default":
        return ResourceQueue.DEFAULT
    return ResourceQueue.HIGH_MEMORY


@pytest.fixture(params=["default", "non_default"])
def pip_extras(request):
    """Extra pip requirements for Node initialization"""
    if request.param == "default":
        return None
    return ["asdf"]


@pytest.fixture(params=["0_upstream", "1_upstream", "2_upstream"])
def node(
    workflow_tasks, request, queue_name, pip_extras
) -> tuple[Node, task_type_hint, Any, str, str]:
    """Node instance and its component parts."""
    version = "V6-123"
    name = f"{request.param}_{version}"
    TaskA, TaskB, TaskC, _ = workflow_tasks
    upstreams = {
        "0_upstream": (None, []),
        "1_upstream": (TaskB, [TaskB]),
        "2_upstream": ([TaskB, TaskC], [TaskB, TaskC]),
    }
    upstream = upstreams[request.param]
    package = __package__
    return (
        Node(
            workflow_name=name,
            workflow_version=version,
            workflow_package=package,
            task=TaskA,
            upstreams=upstream[0],
            resource_queue=queue_name,
            pip_extras=pip_extras,
        ),
        TaskA,
        upstream[1],
        name,
        version,
    )


@pytest.fixture()
def fake_producer():
    return MagicMock(spec=DurableProducer)


@pytest.fixture()
def fake_producer_factory(fake_producer):
    @contextmanager
    def fake_factory():
        try:
            yield fake_producer
        finally:
            pass

    return fake_factory
