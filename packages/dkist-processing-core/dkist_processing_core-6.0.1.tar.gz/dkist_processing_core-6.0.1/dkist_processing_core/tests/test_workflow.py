"""Tests for the Workflow abstraction."""

import json
from typing import Callable

import pytest
from airflow import DAG

from dkist_processing_core import ResourceQueue
from dkist_processing_core import Workflow
from dkist_processing_core.workflow import MAXIMUM_ALLOWED_WORKFLOW_NAME_LENGTH
from dkist_processing_core.workflow import workflow_name_from_details


def test_workflow_metadata(workflow):
    """
    Given: A workflow instance.
    When: accessing attributes.
    Then: Tha values are properly assigned.
    """
    (
        workflow_instance,
        input_data,
        output_data,
        category,
        detail,
        version,
        tags,
    ) = workflow

    assert workflow_instance.workflow_name == f"{input_data}_to_{output_data}_{category}_{detail}"
    assert workflow_instance.workflow_version == version
    assert workflow_instance.workflow_package.startswith(__package__.split(".")[0])
    assert workflow_instance.nodes == []
    assert isinstance(workflow_instance._dag, DAG)
    assert (
        workflow_instance._dag.dag_id
        == f"{input_data}_to_{output_data}_{category}_{detail}_{version}"
    )
    assert workflow_instance.category == category
    assert workflow_instance.input_data == input_data
    assert workflow_instance.output_data == output_data
    assert workflow_instance.detail == detail
    assert sorted(json.loads(workflow_instance.dag_tags)) == sorted(
        [tag for tag in tags] + [input_data, output_data, category, version]
    )


@pytest.mark.parametrize(
    "queue",
    [
        pytest.param(None, id="None"),
        pytest.param(ResourceQueue.HIGH_MEMORY, id="Specified"),
    ],
)
def test_workflow_add_node(workflow_tasks, workflow, queue):
    """
    Given: A set of tasks and a workflow instance.
    When: Adding the tasks to the workflow in the
      structure of A >> [B, C] >> D.
    Then: the dag object owned by the workflow has the right structure.
    """
    (
        workflow_instance,
        process_input,
        process_output,
        process_category,
        process_detail,
        version,
        tags,
    ) = workflow
    TaskA, TaskB, TaskC, TaskD = workflow_tasks
    task_definitions = {
        TaskA: None,  # none
        TaskB: TaskA,  # single
        TaskC: TaskA,  # single
        TaskD: [TaskB, TaskC],  # list
    }
    task_upstream_expectations = {
        TaskA.__name__: set(),
        TaskB.__name__: {
            TaskA.__name__,
        },
        TaskC.__name__: {
            TaskA.__name__,
        },
        TaskD.__name__: {
            TaskB.__name__,
            TaskC.__name__,
        },
    }
    for task, upstream in task_definitions.items():
        workflow_instance.add_node(task, resource_queue=queue, upstreams=upstream)

    dag = workflow_instance.load()
    assert dag.task_count == 4
    assert len(workflow_instance.nodes) == 4

    for task in dag.tasks:
        assert (
            task.dag_id
            == f"{process_input}_to_{process_output}_{process_category}_{process_detail}_{version}"
        )
        assert task.upstream_task_ids == task_upstream_expectations[task.task_id]

    ordered_nodes = workflow_instance.topological_sort()
    assert [node.task for node in ordered_nodes] == [TaskA, TaskB, TaskC, TaskD]


def test_workflow_name_too_long():
    """
    Given: A workflow instance with a long name.
    When: Accessing the workflow_name attribute.
    Then: Get a ValueError.
    """
    with pytest.raises(ValueError):
        Workflow(
            input_data="".join(["a" for _ in range(MAXIMUM_ALLOWED_WORKFLOW_NAME_LENGTH)]),
            output_data="",
            category="",
            detail="",
            workflow_version="",
            workflow_package=__package__,
            tags="",
        )


def test_invalid_workflow_add_node(workflow):
    """
    Given: An invalid task (not inheriting from TaskBase)and a workflow instance.
    When: Adding the task to the workflow.
    Then: Get a TypeError.
    """
    workflow_instance, *args = workflow

    class Task:
        pass

    with pytest.raises(TypeError):
        workflow_instance.add_node(Task)


@pytest.mark.parametrize(
    "func, attr",
    [
        pytest.param(repr, "__repr__", id="repr"),
        pytest.param(str, "__str__", id="str"),
    ],
)
def test_workflow_dunder(workflow, func: Callable, attr):
    """
    Given: workflow instance.
    When: retrieving dunder method that should be implemented.
    Then: It is implemented.
    """
    workflow_instance, *args = workflow

    assert getattr(workflow_instance, attr, None)
    assert func(workflow_instance)


def test_check_dag_name_characters():
    """
    Given: a dag name
    When: checking if it is a valid airflow name or not
    Then: correctly identify valid and invalid names
    """
    Workflow.check_dag_name_characters(dag_name="This_dag_name_is_valid")
    with pytest.raises(ValueError):
        Workflow.check_dag_name_characters(dag_name="Invalid*dag*name")


@pytest.mark.parametrize(
    "detail",
    [
        pytest.param(None, id="no_detail"),
        pytest.param("detail", id="with_detail"),
    ],
)
def test_workflow_name_from_details(detail: str | None):
    """
    Given: a set of details
    When: creating a workflow name
    Then: the workflow name is created correctly
    """
    input_data = "input"
    output_data = "output"
    category = "instrument"
    expected_workflow_name = f"{input_data}_to_{output_data}_{category}"
    if detail:
        expected_workflow_name += f"_{detail}"
    workflow_name = workflow_name_from_details(
        input_data=input_data,
        output_data=output_data,
        category=category,
        detail=detail,
    )
    assert workflow_name == expected_workflow_name


def test_workflow_name_from_details_too_long():
    """
    Given: workflow details with a long input_data value
    When: calling workflow_name_from_details
    Then: a ValueError is raised
    """

    with pytest.raises(ValueError):
        workflow_name = workflow_name_from_details(
            input_data="".join(["a" for _ in range(MAXIMUM_ALLOWED_WORKFLOW_NAME_LENGTH)]),
            output_data="",
            category="",
        )
