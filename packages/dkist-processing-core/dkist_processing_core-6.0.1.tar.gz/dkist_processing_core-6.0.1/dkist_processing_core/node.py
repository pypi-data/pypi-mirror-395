"""Abstraction layer to construct a workflow node using and airflow operator."""

from collections.abc import Iterable
from typing import Type

from airflow.operators.bash import BashOperator

from dkist_processing_core.resource_queue import ResourceQueue
from dkist_processing_core.task import TaskBase

task_type_hint = Type[TaskBase]
upstreams_type_hint = list[task_type_hint] | task_type_hint | None


class Node:
    """Abstraction to instantiate a Task in a Workflow graph for target execution environments."""

    def __init__(
        self,
        workflow_name: str,
        workflow_version: str,
        workflow_package: str,
        task: task_type_hint,
        resource_queue: ResourceQueue,
        upstreams: upstreams_type_hint = None,
        pip_extras: list[str] | None = None,
    ):
        """Node setup."""
        # Task type checking
        upstreams = upstreams or []
        if not isinstance(upstreams, Iterable):
            upstreams = [
                upstreams,
            ]
        if not all([issubclass(t, TaskBase) for t in [task] + upstreams]):
            raise TypeError(
                "Only task classes inheriting from "
                "dkist_processing_core.TaskBase can be added to a workflow"
            )

        self.workflow_name = workflow_name
        self.workflow_version = workflow_version
        self.task = task
        self.workflow_package = workflow_package
        self.upstreams = upstreams
        self.resource_queue = resource_queue
        self.pip_extras = ["frozen"] + (pip_extras or [])

    @property
    def operator(self) -> BashOperator:
        """Native engine node."""
        from datetime import timedelta
        from functools import partial

        from dkist_processing_core.failure_callback import chat_ops_notification

        return eval(self.operator_definition)

    @property
    def notebook_cell(self) -> str:
        """Render the node as python code for a notebook cell."""
        lines = [
            f"from {self.task.__module__} import {self.task.__name__}",
            f"with {self.task.__name__}(recipe_run_id=recipe_run_id, workflow_name='{self.workflow_name}', workflow_version='{self.workflow_version}') as t:\n    #t.is_task_manual = True\n    t()\n    #t.rollback()",
        ]
        return "\n".join(lines)

    @property
    def operator_definition(self) -> str:
        """Airflow style command to define a bash operator."""
        return f"""BashOperator(
    task_id='{self.task.__name__}',
    bash_command='''{self.bash_script}''',
    retries={self.task.retries},
    retry_delay=timedelta(seconds={self.task.retry_delay_seconds}),
    on_failure_callback=partial(
        chat_ops_notification,
        workflow_name='{self.workflow_name}',
        workflow_version='{self.workflow_version}',
        task_name='{self.task.__name__}'
    ),
    owner="DKIST Data Center",
    queue="{self.resource_queue.value}",
    output_processor=str,
)
"""

    @property
    def dependencies(self) -> list[tuple[str, str]]:
        """List of upstream, downstream task name tuples."""
        return [(upstream.__name__, self.task.__name__) for upstream in self.upstreams]

    @property
    def bash_script(self) -> str:
        """Format bash script for the BashOperator."""
        command = f"""{self.install_command}
echo Virtual Python Environment Packages
pip list
{self.run_command}"""
        return self.bash_template(command)

    @staticmethod
    def bash_template(command: str) -> str:
        """Return the bash script with a template wrapped command."""
        return f"""#!/bin/bash
echo Working Directory
pwd
echo Worker Identification
echo NOMAD_ALLOC_ID
echo $NOMAD_ALLOC_ID
echo NOMAD_GROUP_NAME
echo $NOMAD_GROUP_NAME
echo NOMAD_HOST_ADDR_worker
echo $NOMAD_HOST_ADDR_worker
echo NOMAD_ALLOC_NAME
echo $NOMAD_ALLOC_NAME
echo Host Python Environment i.e. system-site-packages
python3 -m pip install --upgrade --user pip
pip list
echo Creating Virtual Environment
python3 -m venv .task_venv
echo Activate Environment
. .task_venv/bin/activate
echo Python Interpreter Location
which python
echo Run Main Command
{command}
export exit_code=$?
echo Deactivate Environment
deactivate
echo Remove Virtual Environment
rm -rf .task_venv
echo Exit with code from main command: $exit_code
exit $exit_code"""

    @property
    def formatted_pip_extras(self) -> str:
        """Format pip extras for the installation command."""
        if self.pip_extras:
            extra_requirements = ",".join(self.pip_extras)
            return f"'[{extra_requirements}]'"
        return ""

    @property
    def install_command(self) -> str:
        """Format the installation command for the bash script."""
        repo_name = self.workflow_package.split(".")[0].replace("_", "-")
        version = self.workflow_version
        extras = self.formatted_pip_extras
        return f"""python -m pip install --upgrade pip
python -m pip install {repo_name}{extras}=={version}"""

    @property
    def run_command(self) -> str:
        """Return the python bash command to execute the task."""
        return f'python -c "{self.python}"'

    @property
    def python(self) -> str:
        """Return the python code to execute the task."""
        return f"""from {self.task.__module__} import {self.task.__name__}
with {self.task.__name__}(recipe_run_id={{{{dag_run.conf['recipe_run_id']}}}}, workflow_name='{self.workflow_name}', workflow_version='{self.workflow_version}') as task:
    task()
"""

    def __repr__(self):
        """Render node instantiation as a string."""
        return f"Node(workflow_name={self.workflow_name}, workflow_version={self.workflow_version}, workflow_package={self.workflow_package}, task={self.task!r}, upstreams={self.upstreams}, queue={self.resource_queue!r})"

    def __str__(self):
        """Render node instance as a string."""
        return repr(self)
