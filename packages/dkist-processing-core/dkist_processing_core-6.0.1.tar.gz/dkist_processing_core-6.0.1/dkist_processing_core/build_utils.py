"""Utilities for the build pipeline."""

import importlib
from pathlib import Path
from shutil import rmtree
from types import ModuleType

from dkist_processing_core import Workflow

__all__ = ["validate_workflows", "export_dags", "export_notebook_dockerfile", "export_notebooks"]


def validate_workflows(workflow_package: ModuleType, export_path: Path | None = None) -> None:
    """Validate that workflow engine (airflow) objects are acyclic and that exported workflows compile."""
    # configure export path.  Clean up after if export path not provided
    rm_export_path_after_test = not bool(export_path)
    if export_path is None:
        export_path = Path("export/")
    workflows = extract_workflows_from_package(workflow_package)
    try:
        _validate_workflows(workflows, export_path)
    finally:
        if rm_export_path_after_test:
            rmtree(export_path)


def _validate_workflows(workflows: list[Workflow], export_path: Path) -> None:
    """Validate workflows by ensuring their exported version compiles as python and that there is at least one node."""
    for w in workflows:
        workflow_py = w.export_dag(path=export_path)
        with workflow_py.open(mode="r") as f:
            compile(f.read(), filename=f"{workflow_py.stem}.pyc", mode="exec")
        if len(w.nodes) == 0:
            raise ValueError(f"Workflow {w.workflow_name} has 0 nodes.")


def export_dags(workflow_package: ModuleType, path: str | Path) -> list[Path]:
    """Export Airflow DAG files."""
    return [w.export_dag(path=path) for w in extract_workflows_from_package(workflow_package)]


def export_notebooks(workflow_package: ModuleType, path: str | Path) -> list[Path]:
    """Export Jupyter Notebook files."""
    return [w.export_notebook(path=path) for w in extract_workflows_from_package(workflow_package)]


def export_notebook_dockerfile(workflow_package: ModuleType, path: str | Path) -> Path:
    """Export a dockerfile to containerize notebooks."""
    path = Path(path)
    notebook_paths = export_notebooks(workflow_package=workflow_package, path=path)
    category = extract_category_from_workflows(workflow_package=workflow_package)
    dockerfile = NotebookDockerfile(notebook_paths=notebook_paths, category=category)
    dockerfile_path = Path("Dockerfile")
    dockerfile_path.touch(exist_ok=False)
    with open(dockerfile_path, mode="w") as f:
        f.write(dockerfile.contents)
    return dockerfile_path


def extract_category_from_workflows(workflow_package: ModuleType) -> str:
    """Extract the category from the workflows in the package to provide a unique category for the dockerfile."""
    workflows = extract_workflows_from_package(workflow_package)
    categories = {w.category for w in workflows}
    if len(categories) > 1:
        raise ValueError(
            f"Multiple categories found in provided workflows. Categories found: {categories}"
        )
    return categories.pop()


def extract_workflows_from_package(workflow_package: ModuleType) -> list[Workflow]:
    """Extract all the Workflow objects from a package."""
    return extract_objects_from_package_by_type(workflow_package, Workflow)


def extract_objects_from_package_by_type(package: ModuleType, object_type: type) -> list:
    """Extract all objects in public modules of a given type from a package."""
    modules = parse_unprotected_modules_names_from_package(package)
    objects = []
    for module in modules:
        imported_module = importlib.import_module(f".{module}", package.__name__)
        objects += [var for var in vars(imported_module).values() if isinstance(var, object_type)]
    return objects


def parse_unprotected_modules_names_from_package(package: ModuleType) -> list[str]:
    """Parse the names of all modules in a package that are not private i.e. don't begin with an underscore."""
    package_path = Path(package.__path__[0])
    return [m.stem for m in package_path.glob("[!_]*.py")]


class NotebookDockerfile:
    """Build a Dockerfile for deployment as a Manual Processing Worker."""

    def __init__(self, notebook_paths: list[Path], category: str):
        self.notebook_paths = notebook_paths
        self.validate_notebook_paths_are_relative()
        self.category = category

    def validate_notebook_paths_are_relative(self):
        """Validate that the notebook paths are all relative."""
        return all([not p.is_absolute() for p in self.notebook_paths])

    @property
    def contents(self) -> str:
        """Return the Dockerfile body."""
        return "\n".join(self.preamble + self.setup + self.notebooks + self.command)

    @property
    def preamble(self) -> list[str]:
        """Dockerfile preamble lines."""
        return ["FROM python:3.12", "ENV LANG=C.UTF-8"]

    @property
    def setup(self) -> list[str]:
        """Environment setup lines."""
        return [
            "COPY . /app",
            "WORKDIR /app",
            "RUN python -m pip install -U pip",
            "RUN pip install notebook",
            "RUN pip freeze | grep notebook= > constraints.txt",
            "RUN cat constraints.txt",
            "RUN python -m pip install -c constraints.txt .",
        ]

    @property
    def notebooks(self) -> list[str]:
        """Generate workflow notebooks and include in Docker container."""
        return [f"COPY {notebook_path} /notebooks/" for notebook_path in self.notebook_paths]

    @property
    def command(self) -> list[str]:
        """Run notebook server on deployment."""
        port = 8888
        return [
            f"EXPOSE {port}",
            f"CMD jupyter notebook --NotebookApp.allow_root=True --NotebookApp.base_url='/mpw-{self.category}/' --NotebookApp.ip='0.0.0.0' --NotebookApp.port={port} --MappingKernelManager.cull_idle_timeout=300 --notebook-dir=/notebooks --allow-root",
        ]
