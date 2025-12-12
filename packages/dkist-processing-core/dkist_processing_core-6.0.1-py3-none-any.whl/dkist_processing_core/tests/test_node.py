"""Tests of the node.py module."""

import subprocess
from subprocess import CalledProcessError
from typing import Callable

import pytest
from airflow.operators.bash import BashOperator
from jinja2 import Template

from dkist_processing_core import ResourceQueue
from dkist_processing_core.node import Node
from dkist_processing_core.tests.task_example import Task


@pytest.fixture()
def single_node_version() -> str:
    return "3.4.5"


@pytest.fixture()
def single_node(pip_extras, single_node_version) -> Node:
    """A single Node instance."""
    return Node(
        workflow_name="test_node",
        workflow_version=single_node_version,
        workflow_package=__package__,
        task=Task,
        resource_queue=ResourceQueue.DEFAULT,
        pip_extras=pip_extras,
    )


def test_nodes(node, fake_producer_factory, queue_name, pip_extras):
    """
    Given: Workflow tasks to initialize a Node.
    When: Initializing the Node with valid task and upstreams.
    Then: Node properties are created as expected.
    """
    node, task, upstream, name, version = node
    operator = node.operator
    failure_callback_func = operator.on_failure_callback
    assert callable(failure_callback_func)
    # passing in just a context dict positional arg with a fake http adapter does not raise an error
    failure_callback_func({"context": True}, producer_factory=fake_producer_factory)
    assert isinstance(operator, BashOperator)
    assert node.install_command in operator.bash_command
    assert node.python in operator.bash_command
    assert node.workflow_name == name
    assert node.upstreams == upstream
    assert node.task == task
    assert node.workflow_version == version
    assert node.resource_queue == queue_name
    assert node.pip_extras == ["frozen"] + (pip_extras or [])


def test_node_install_command(single_node, pip_extras, single_node_version):
    """
    Given: A valid node instance.
    When: Creating the pip install commands with and without pip extras
    Then: The correct command is generated; pip extras are installed separately from the "frozen" extra
    """
    expected_repo_name = __package__.split(".")[0].replace("_", "-")
    extras_str = f"'[{','.join(['frozen'] + (pip_extras or []))}]'"
    expected_install_command = f"""python -m pip install --upgrade pip
python -m pip install {expected_repo_name}{extras_str}=={single_node_version}"""

    assert single_node.install_command == expected_install_command


@pytest.mark.long()
def test_node_bash_template_return_0(node):
    """
    Given: A valid node instance.
    When: Running the bash script template WITHOUT an error producing python call.
    Then: It returns a 0.
    """
    node, *args = node
    cmd = 'python -c "pass"'
    result = subprocess.run(node.bash_template(cmd), shell=True, check=True)
    assert result.returncode == 0


@pytest.mark.long()
def test_node_bash_template_return_1(node):
    """
    Given: A valid node instance.
    When: Running the bash script template WITH an error producing python call.
    Then: It returns a 1.
    """
    node, *args = node
    cmd = 'python -c "raise Exception"'
    with pytest.raises(CalledProcessError):
        subprocess.run(node.bash_template(cmd), shell=True, check=True)


def test_node_python(single_node):
    """
    Given: Python jinja rendered with dag run data from a node instance.
    When: parsing the python call.
    Then: no exceptions raised.
    """
    # Given
    code_template = Template(single_node.python)

    class RenderData:
        def __init__(self):
            self.conf = {"recipe_run_id": 100}

    dag_run = RenderData()
    rendered_code = code_template.render(dag_run=dag_run)

    # When
    compile(rendered_code, filename="node_test.pyc", mode="exec")
    # Then
    assert True  # exception not raised from compile


def test_invalid_node(task_subclass):
    """
    Given: An invalid task (not inheriting from TaskBase).
    When: Create a Node with that Task.
    Then: Get a TypeError.
    """

    class GoodTask(task_subclass):
        pass

    class BadTask:
        pass

    with pytest.raises(TypeError):
        Node(workflow_name="bad_task", workflow_package=__package__, task=BadTask)

    with pytest.raises(TypeError):
        Node(
            workflow_name="bad_upstream",
            workflow_package=__package__,
            task=GoodTask,
            upstreams=BadTask,
        )

    with pytest.raises(TypeError):
        Node(
            workflow_name="bad_upstream2",
            workflow_package=__package__,
            task=GoodTask,
            upstreams=[GoodTask, BadTask],
        )


@pytest.mark.parametrize(
    "func, attr",
    [
        pytest.param(repr, "__repr__", id="repr"),
        pytest.param(str, "__str__", id="str"),
    ],
)
def test_node_dunder(single_node, func: Callable, attr: str):
    """
    Given: Node instance
    When: retrieving dunder method that should be implemented.
    Then: It is implemented.
    """
    assert getattr(single_node, attr, None)
    assert func(single_node)


def test_node_notebook_cell(single_node):
    """
    Given: a node
    When: rendering that node into python code for inclusion in a notebook
    Then: the code compiles without error
    """
    exec_string = f"recipe_run_id = 1\n{single_node.notebook_cell}"
    exec(exec_string)
