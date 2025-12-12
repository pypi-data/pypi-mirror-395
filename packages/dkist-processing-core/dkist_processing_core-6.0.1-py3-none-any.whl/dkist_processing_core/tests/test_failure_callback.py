"""Test for the failure callback function."""

import pytest
from talus import DurableProducer

from dkist_processing_core.failure_callback import RecipeRunFailureMessage
from dkist_processing_core.failure_callback import chat_ops_notification
from dkist_processing_core.failure_callback import parse_dag_run_id_from_context
from dkist_processing_core.failure_callback import parse_log_url_from_context
from dkist_processing_core.failure_callback import recipe_run_failure_message_producer_factory


@pytest.fixture()
def context(task_instance) -> dict:
    """Task instance context dict."""
    return {"context": True, "run_id": "QAZXYV_1", "task_instance": task_instance}


def test_recipe_run_failure_producer_factory():
    """
    Given: recipe_run_failure_producer_factory.
    When: retrieving a producer from the factory.
    Then: it is an instance of a talus.DurableBlockingProducerWrapper.
    """
    with recipe_run_failure_message_producer_factory() as producer:
        assert isinstance(producer, DurableProducer)


def test_parse_dag_run_id_from_context(context):
    """
    Given: a context dictionary.
    When: parsing the context dict.
    Then: run_id is extracted and returned.
    """
    actual = parse_dag_run_id_from_context(context)
    assert actual == context["run_id"]


def test_parse_log_url_from_context(context):
    """
    Given: a context dictionary.
    When: parsing the context dict.
    Then: run_id is extracted and returned.
    """
    actual = parse_log_url_from_context(context)
    assert actual == context["task_instance"].log_url


def test_chat_ops_notification(fake_producer_factory, context, fake_producer):
    """
    Given: A fake producer factory to capture the publishing from a chat ops notification and fake parameters.
    When: call is made to chat ops notification.
    Then: Expected message was published
    """
    workflow_name = "wkflow"
    workflow_version = "ver"
    task_name = "task"
    message = chat_ops_notification(
        context=context,
        workflow_name=workflow_name,
        workflow_version=workflow_version,
        task_name=task_name,
        producer_factory=fake_producer_factory,
    )
    assert isinstance(message, RecipeRunFailureMessage)
    assert message.body.workflowName == workflow_name
    assert message.body.workflowVersion == workflow_version
    assert message.body.taskName == task_name
    assert message.body.logUrl == context["task_instance"].log_url
    assert message.body.conversationId
    assert message.body.dagRunId == context["run_id"]
    fake_producer.publish.assert_called_once()


def test_chat_ops_notification_no_raise():
    """
    Given: chat_ops_notification function.
    When: call is made to chat ops notification.
    Then: No error raised.
    """
    workflow_name = "wkflow"
    workflow_version = "ver"
    task_name = "task"
    context = {"context": True, "run_id": "QAZXYV_1"}
    # no errors raised
    chat_ops_notification(
        context=context,
        workflow_name=workflow_name,
        workflow_version=workflow_version,
        task_name=task_name,
    )
