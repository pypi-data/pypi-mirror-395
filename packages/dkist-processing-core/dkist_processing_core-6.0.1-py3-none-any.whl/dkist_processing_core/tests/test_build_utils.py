"""Tests for the build utils."""

import os
import subprocess
from pathlib import Path
from shutil import rmtree

import pytest
from airflow.exceptions import AirflowException
from airflow.exceptions import DuplicateTaskIdFound

from dkist_processing_core.build_utils import export_dags
from dkist_processing_core.build_utils import export_notebook_dockerfile
from dkist_processing_core.build_utils import export_notebooks
from dkist_processing_core.build_utils import validate_workflows
from dkist_processing_core.tests import invalid_workflow_cyclic
from dkist_processing_core.tests import invalid_workflow_for_docker_multi_category
from dkist_processing_core.tests import valid_workflow_package
from dkist_processing_core.tests import zero_node_workflow_package


def test_validate_workflow_valid():
    """
    Given: A workflow package with a valid workflow.
    When: validating the workflow.
    Then: No errors raised.
    """
    validate_workflows(valid_workflow_package)


@pytest.mark.parametrize(
    "workflow_package",
    [
        invalid_workflow_cyclic,
        zero_node_workflow_package,
    ],
)
def test_validate_workflow_invalid(workflow_package):
    """
    Given: A workflow package with an invalid workflow.
    When: validating the workflow.
    Then: Errors raised.
    """
    exceptions = (ValueError, DuplicateTaskIdFound)
    with pytest.raises(exceptions):
        validate_workflows(workflow_package)


def test_validate_workflow_zero_nodes():
    """
    Given: A workflow package with an invalid workflow of zero nodes.
    When: validating the workflow.
    Then: Errors raised.
    """
    exceptions = (ValueError, AirflowException)
    with pytest.raises(exceptions):
        validate_workflows(zero_node_workflow_package)


def test_export_dag(export_path):
    """
    Given: A path to export to and a package containing a valid workflow.
    When: Workflows in the package are exported.
    Then: Expected export file exists.
    """
    export_dags(valid_workflow_package, export_path)
    path = export_path / Path("test-data_to_valid_core_dev.py")
    assert path.exists()


def test_export_notebook(export_path):
    """
    Given: A path to export to and a package containing a valid workflow.
    When: Workflows in the package are exported as ipynb.
    Then: Expected export files exists.
    """
    paths = export_notebooks(valid_workflow_package, export_path)
    assert len(paths) >= 1
    assert all([p.exists() for p in paths])


@pytest.fixture()
def repository_root_path() -> Path:
    """Return a directory relative to repository root"""
    repo_root_parts = []
    cwd = Path.cwd()  # expecting to be 2 levels below repo root
    for part in cwd.parts:
        repo_root_parts.append(part)
        if part == "dkist-processing-core":
            break
    return Path(*repo_root_parts)


@pytest.fixture()
def notebook_export_path(repository_root_path) -> Path:
    """Return a directory relative to repository root"""
    export_path = Path("notebooks/")
    yield Path("notebooks/")
    rmtree(export_path, ignore_errors=True)


@pytest.mark.long()
def test_export_notebook_dockerfile(repository_root_path, notebook_export_path):
    """
    Given: A path to export to and a package containing a valid workflow.
    When: Workflows in the package are exported as a valid Dockerfile.
    Then: Expected export file exists.
    """
    os.chdir(str(repository_root_path))
    print(Path.cwd())
    dockerfile_path = export_notebook_dockerfile(valid_workflow_package, notebook_export_path)
    assert dockerfile_path.exists()
    image_name = "test_export_notebook_dockerfile:latest"
    subprocess.run(["docker", "build", "-t", image_name, dockerfile_path.parent], check=True)
    dockerfile_path.unlink()


@pytest.mark.long()
def test_export_notebook_dockerfile_invalid_workflow_package(
    repository_root_path, notebook_export_path
):
    """
    Given: A path to export to and a package containing a valid workflow.
    When: Workflows in the package are exported as a valid Dockerfile.
    Then: Expected export file exists.
    """
    os.chdir(str(repository_root_path))
    with pytest.raises(ValueError):
        export_notebook_dockerfile(invalid_workflow_for_docker_multi_category, notebook_export_path)
