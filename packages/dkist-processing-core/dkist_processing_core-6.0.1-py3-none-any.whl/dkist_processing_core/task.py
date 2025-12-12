"""
Base class that is used to wrap the various DAG task methods.

It provides support for user-defined setup and cleanup, task monitoring using OpenTelemetry,
standardized logging, and exception handling.
"""

import logging
from abc import ABC
from abc import abstractmethod
from contextlib import contextmanager
from typing import Generator
from typing import Sequence

from opentelemetry.context.context import Context
from opentelemetry.metrics import Counter
from opentelemetry.metrics import Meter
from opentelemetry.trace import Link
from opentelemetry.trace import Span
from opentelemetry.trace import SpanKind
from opentelemetry.trace import StatusCode
from opentelemetry.trace import Tracer
from opentelemetry.util.types import Attributes

from dkist_processing_core.config import core_configurations

__all__ = ["TaskBase"]

logger = logging.getLogger(__name__)


class TaskBase(ABC):
    """
    A Task is the interface between processing code and its execution.  Processing code can follow this interface through subclassing remain agnostic to the execution environment.

    Each DAG task must implement its own subclass of this abstract wrapper class.

    Intended instantiation is as a context manager

    >>> class RealTask(TaskBase):
    >>>     def run(self):
    >>>         pass
    >>>
    >>> with RealTask(1, "a", "b") as task:
    >>>     task()

    Task names in airflow are the same as the class name
    Additional methods can be added but will only be called if they are referenced via run,
    pre_run, post_run, or __exit__

    overriding methods other than run, pre_run, post_run, and in special cases __exit__ is
    discouraged as they are used internally to support the abstraction.
    e.g. __init__ is called by the core api without user involvement so adding parameters will not
    result in them being passed in as there is no client interface to __init__.

    To use the tracing infrastructure in subclass code one would do the following:

    >>> def foo(self):
    >>>     with self.telemetry_span("do detailed work"):
    >>>         pass # do work

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    retries = 0
    retry_delay_seconds = 60
    tracer: Tracer = core_configurations.tracer
    meter: Meter = core_configurations.meter

    def __init__(
        self,
        recipe_run_id: int,
        workflow_name: str,
        workflow_version: str,
    ):
        """
        Instantiate a Task.

        The details of instantiation may vary based upon the export target but this signature is what is expected by the instantiation transformation (Node) code.
        """
        self.recipe_run_id = int(recipe_run_id)
        self.workflow_name = workflow_name
        self.workflow_version = workflow_version
        self.task_name = self.__class__.__name__

        self.base_telemetry_attributes = {
            "recipe.run.id": self.recipe_run_id,
            "workflow.name": self.workflow_name,
            "workflow.version": self.workflow_version,
            "task.name": self.task_name,
            "nomad.allocation.id": core_configurations.allocation_id,
            "nomad.allocation.name": core_configurations.allocation_name,
            "nomad.allocation.group": core_configurations.allocation_group,
        }

        # meter instruments
        self.task_execution_counter: Counter = self.meter.create_counter(
            name=self.format_metric_name("tasks.executed"),
            unit="1",
            description="The number of tasks executed in the processing stack.",
        )

        logger.info(f"Task {self.task_name} initialized")

    @contextmanager
    def telemetry_span(
        self,
        name: str,
        context: Context | None = None,
        kind: SpanKind = SpanKind.INTERNAL,
        attributes: Attributes = None,
        links: Sequence[Link] | None = None,
        start_time: int | None = None,
        record_exception: bool = True,
        set_status_on_exception: bool = True,
        end_on_exit: bool = True,
    ) -> Generator[Span, None, None]:  # noqa: D405,D407
        """
        Context manager for creating a new span and set it as the current span in this tracer's context.

        Parameters
        ----------
        name
            The name of the span to be created.

        context
            An optional Context containing the span's parent. Defaults to the global context.

        kind
            The span's kind (relationship to parent). Note that is meaningful even if there is no parent.

        attributes
            The span's attributes.

        links
            Links span to other spans

        start_time
            Sets the start time of a span

        record_exception
            Whether to record any exceptions raised within the context as error event on the span.

        set_status_on_exception
            Only relevant if the returned span is used in a with/context manager. Defines whether the span status will
            be automatically set to ERROR when an uncaught exception is raised in the span with block. The span status
            won't be set by this mechanism if it was previously set manually.

        end_on_exit
            Whether to end the span automatically when leaving the context manager.

        Yields
        ------
        The newly-created span.
        """
        with self.tracer.start_as_current_span(
            name=name,
            context=context,
            kind=kind,
            attributes=attributes,
            links=links,
            start_time=start_time,
            record_exception=record_exception,
            set_status_on_exception=set_status_on_exception,
            end_on_exit=end_on_exit,
        ) as span:
            span.set_attributes(self.base_telemetry_attributes)
            yield span
            span.set_status(StatusCode.OK)

    def format_metric_name(self, name: str) -> str:
        """
        Format the metric name to include the meter name and a namespace of 'processing' for dkist-processing-* meters. Words are separated by a dot.

        For example, if the meter name is "dkist.meter" and the metric name is "tasks.executed",
        the formatted name will be "dkist.meter.processing.tasks.executed".
        """
        return f"{self.meter.name}.processing.{name}"

    def pre_run(self) -> None:
        """Intended to be overridden and will execute prior to run() with Open Telemetry trace span capturing."""

    @abstractmethod
    def run(self) -> None:
        """Abstract method that must be overridden to execute the desired DAG task with Open Telemetry trace span capturing."""

    def post_run(self) -> None:
        """Intended to be overridden and will execute after run() with Open Telemetry trace span capturing."""

    def rollback(self) -> None:
        """Rollback any changes to persistent stores performed by the task."""

    def __call__(self) -> None:
        """
        DAG task wrapper. Execution is instrumented with Open Telemetry tracing if configured.

        The standard execution sequence is:

        1 run

        2 record provenance

        Returns
        -------
        None

        """
        verbose_task_name = f"{self.workflow_name}.{self.task_name}"
        logger.info(f"{verbose_task_name} started")

        self.task_execution_counter.add(amount=1, attributes=self.base_telemetry_attributes)

        with self.telemetry_span(f"{verbose_task_name}") as span:  # Root Span
            span.set_attribute("dkist.root", "True")
            with self.telemetry_span("Pre Run"):
                self.pre_run()
            with self.telemetry_span("Run"):
                self.run()
            with self.telemetry_span("Post Run"):
                self.post_run()
        logger.info(f"{verbose_task_name} complete")

    def __enter__(self):
        """
        Override to execute setup tasks before task execution.

        Only override this method with tasks that need to happen
        regardless of tasks having an exception, ensure that no additional exception
        will be raised, and always call super().__enter__
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Override to execute teardown tasks after task execution regardless of task execution success.

        Only override this method with tasks that need to happen
        regardless of tasks having an exception, ensure that no additional exception
        will be raised, and always call super().__exit__
        """

    def __repr__(self):
        """Return the representation of the task."""
        return (
            f"{self.__class__.__name__}("
            f"recipe_run_id={self.recipe_run_id}, "
            f"workflow_name={self.workflow_name}, "
            f"workflow_version={self.workflow_version}, "
            f")"
        )

    def __str__(self):
        """Return a string representation of the task."""
        return repr(self)
