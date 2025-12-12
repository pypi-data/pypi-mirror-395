"""Define the failure callback functionality."""

import logging
from contextlib import contextmanager
from typing import Callable
from typing import Generator
from typing import Type

from talus import Binding
from talus import DurableProducer
from talus import MessageBodyBase
from talus import PublishMessageBase
from talus import Queue

from dkist_processing_core.config import core_configurations

logger = logging.getLogger(__name__)


# Recipe run failure message Definition
class RecipeRunFailureMessageBody(MessageBodyBase):
    """Schema for the recipe run failure message body."""

    workflowName: str
    workflowVersion: str
    taskName: str
    dagRunId: str | None = None
    logUrl: str | None = None


class RecipeRunFailureMessage(PublishMessageBase):
    """Recipe run failure message including the message body and other publication information."""

    message_body_cls: Type[RecipeRunFailureMessageBody] = RecipeRunFailureMessageBody
    default_routing_key: str = "recipe.run.failure.m"


@contextmanager
def recipe_run_failure_message_producer_factory() -> Generator[DurableProducer, None, None]:
    """Create message producer for recipe run failure messages."""
    # Configure the queue the messages should be routed to
    recipe_run_failure_queue = Queue(
        name="recipe.run.failure.q", arguments=core_configurations.isb_queue_arguments
    )
    # Configure the exchange and queue bindings for publishing
    bindings = [Binding(queue=recipe_run_failure_queue, message=RecipeRunFailureMessage)]
    try:
        with DurableProducer(
            queue_bindings=bindings,
            publish_exchange=core_configurations.isb_publish_exchange,
            connection_parameters=core_configurations.isb_producer_connection_parameters,
            connection_retryer=core_configurations.isb_connection_retryer,
        ) as producer:
            yield producer
    finally:
        pass


def parse_dag_run_id_from_context(context: dict) -> str | None:
    """Find dag run id."""
    return context.get("run_id", None)


def parse_log_url_from_context(context: dict) -> str | None:
    """Given an airflow context, find the URL of the logs created by the task."""
    ti = context.get("task_instance", object)
    try:
        return ti.log_url
    except AttributeError:
        pass


def chat_ops_notification(
    context: dict,
    workflow_name: str,
    workflow_version: str,
    task_name: str,
    producer_factory: Callable[[], DurableProducer] = recipe_run_failure_message_producer_factory,
) -> RecipeRunFailureMessage:
    """Publish message with information regarding a task failure for publication to a chat service."""
    dag_run_id = parse_dag_run_id_from_context(context)
    log_url = parse_log_url_from_context(context)
    body = RecipeRunFailureMessageBody(
        workflowName=workflow_name,
        workflowVersion=workflow_version,
        taskName=task_name,
        logUrl=log_url,
        dagRunId=dag_run_id,
    )
    message = RecipeRunFailureMessage(body)

    try:
        with producer_factory() as producer:
            logger.warning(f"Publishing failure callback message: {message=}")
            producer.publish(message)
            return message
    except Exception as e:  # pragma: no cover
        logger.error(f"Error raised executing failure callback: {e=}")  # pragma: no cover
