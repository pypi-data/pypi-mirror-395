"""Test minimal dependency dag export (used for scheduler deployments)."""

import nbformat
import pytest
from nbconvert import PythonExporter

from dkist_processing_core.tests.task_example import Task
from dkist_processing_core.tests.task_example import Task2
from dkist_processing_core.tests.task_example import Task3
from dkist_processing_core.tests.task_example import Task4


@pytest.fixture
def workflow_to_export(workflow):
    """A workflow instance with tasks in the structure of Task >> [Task2, Task3] >> Task4."""
    (
        workflow_instance,
        input_data,
        output_data,
        category,
        detail,
        version,
        tags,
    ) = workflow
    task_definitions = {
        Task: None,  # none
        Task2: Task,  # single
        Task3: Task,  # single
        Task4: [Task2, Task3],  # list
    }
    for task, upstream in task_definitions.items():
        workflow_instance.add_node(task, upstreams=upstream)
    yield workflow_instance, input_data, output_data, category, detail, version, tags


def test_export_dag(export_path, workflow_to_export):
    """
    Given: A workflow instance with tasks in the structure of A >> [B, C] >> D.
    When: Exporting the dag.
    Then: The exported dag compiles.
    """
    workflow_instance, input_data, output_data, category, detail, version, tags = workflow_to_export
    # When
    dag_file = workflow_instance.export_dag(path=export_path)
    # Then
    with dag_file.open(mode="r") as f:
        compile(
            f.read(),
            filename=f"{input_data}_to_{output_data}_{category}_{detail}_{version}.pyc",
            mode="exec",
        )
    assert True  # exception not raised from compile


def test_export_notebook(workflow_to_export, export_path):
    """
    Given: A workflow instance with tasks in the structure of A >> [B, C] >> D.
    When: Exporting the notebook.
    Then: The exported notebook compiles and runs.
    """
    workflow_instance, input_data, output_data, category, detail, version, tags = workflow_to_export
    # When
    notebook_path = workflow_instance.export_notebook(path=export_path)
    # Then
    with notebook_path.open(mode="r", encoding="utf-8") as f:
        notebook_contents = f.read()
    notebook = nbformat.reads(notebook_contents, as_version=4)
    exporter = PythonExporter()
    python_script: str = exporter.from_notebook_node(notebook)[0]
    python_script = python_script.replace("recipe_run_id: int =", "recipe_run_id: int = 1")
    exec(python_script)
    assert True  # python script didn't raise errors
