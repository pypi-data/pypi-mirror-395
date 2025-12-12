"""Abstraction layer to construct a workflow as an airflow DAG."""

import json
import string
from graphlib import TopologicalSorter
from pathlib import Path

import nbformat as nbf
from airflow import DAG

from dkist_processing_core.config import core_configurations
from dkist_processing_core.node import Node
from dkist_processing_core.node import task_type_hint
from dkist_processing_core.node import upstreams_type_hint
from dkist_processing_core.resource_queue import ResourceQueue

__all__ = ["Workflow", "workflow_name_from_details"]

MAXIMUM_ALLOWED_WORKFLOW_NAME_LENGTH = 100


def workflow_name_from_details(
    input_data: str, output_data: str, category: str, detail: str | None = None
) -> str:
    """Create the workflow name from its constituent parts."""
    workflow_name = f"{input_data}_to_{output_data}_{category}"
    if detail:
        workflow_name += f"_{detail}"
    workflow_name_too_long = len(workflow_name) > MAXIMUM_ALLOWED_WORKFLOW_NAME_LENGTH
    if workflow_name_too_long:
        raise ValueError(
            f"Workflow name {workflow_name} is {len(workflow_name)} characters long. "
            f"Limit is {MAXIMUM_ALLOWED_WORKFLOW_NAME_LENGTH} characters."
        )
    return workflow_name


class Workflow:
    """
    Abstraction to create a workflow in 1 or more target execution environment.

    - Defines the api for task and workflow definition
    - abstracts workflow engine syntax from task definition
    - implements workflow and tasks in engine specific syntax
    - engine = airflow
    - contains nodes and the relationships between them
    - selects the appropriate Node method for task instantiation based upon the export target

    >>> category = "instrument"
    >>> input_data = "l0"
    >>> output_data = "l1"
    >>> detail = "OCP-use-only"
    >>> version = "V6-12342"
    >>> tags = ["use-XYZ-algorithm"]
    >>> task = Task()
    >>> workflow_instance = Workflow(
    >>>    category=category,
    >>>    input_data=input_data,
    >>>    output_data=output_data,
    >>>    detail=detail,
    >>>    workflow_package=__package__,
    >>>    workflow_version=version,
    >>>    tags=tags
    >>>)
    >>> workflow_instance.add_node(task=task, upstreams=None)
    """

    def __init__(
        self,
        *,
        input_data: str,
        output_data: str,
        category: str,
        workflow_package: str,
        detail: str | None = None,
        tags: list[str] | str | None = None,
        workflow_version: str | None = None,
    ):
        """
        Create a workflow instance.

        Parameters
        ----------
        input_data: Description of the primary inputs to the workflow e.g. l0
        output_data: Description of the primary outputs of the workflow e.g. l1
        category: Category for the process the workflow executes e.g. instrument name
        detail: Extra information to separate this workflow from a similar workflow
        workflow_package: The string representing the dot notation location of the
          workflow definition. e.g. __package__
        tags: tags to be used in airflow's UI when searching for dags
        workflow_version: Version of the workflow being deployed.  Typically populated by the CI/CD
          build process.

        """
        self.workflow_package = workflow_package
        self.category = category
        self.input_data = input_data
        self.output_data = output_data
        self.detail = detail
        self.workflow_version = workflow_version or core_configurations.build_version
        if isinstance(tags, str):
            tags = [tags]
        self.tags: list[str] = tags or []
        self._dag = self.initialize_local_dag()
        self.nodes = []

    @property
    def workflow_name(self) -> str:
        """Return the workflow name created from its constituent parts."""
        return workflow_name_from_details(
            input_data=self.input_data,
            output_data=self.output_data,
            category=self.category,
            detail=self.detail,
        )

    @property
    def dag_name(self) -> str:
        """Return the dag name created from its constituent parts."""
        result = f"{self.workflow_name}_{self.workflow_version}"
        self.check_dag_name_characters(result)  # raise an error if in valid
        return result

    @staticmethod
    def check_dag_name_characters(dag_name: str):
        """
        Figure out if the dag name is an Airflow-allowed name.

        Can only contain
        * ascii letters
        * numbers
        * dash (-)
        * dot (.)
        * underscore (_)

        Raise error if non-allowed characters are found.
        """
        allowed_chars = (
            [c for c in string.ascii_letters] + ["-", ".", "_"] + [n for n in string.digits]
        )
        if not all([char in allowed_chars for char in dag_name]):
            raise ValueError(
                f"Dag name {dag_name} contains invalid characters. "
                f"Only ascii letters and the dash, dot, and "
                f"underscore symbols are permitted."
            )

    @property
    def dag_tags(self) -> str:
        """
        Return the list of dag tags to be used in Airflow's UI.

        Equal to the list of supplied tags plus the workflow version, input and output data,
        and category.
        """
        tags = self.tags + [self.workflow_version, self.input_data, self.output_data, self.category]
        # Make sure there are no duplicate tags
        tags = list(set(tags))
        return json.dumps(tags)

    @property
    def dag_definition(self) -> str:
        """Return the string representation of the DAG object instantiation."""
        return f"DAG(dag_id='{self.dag_name}', start_date=pendulum.today('UTC').add(days=-2), schedule=None, catchup=False, tags={self.dag_tags})"

    def initialize_local_dag(self) -> DAG:
        """Create a local instance of the DAG object."""
        import pendulum

        return eval(self.dag_definition)

    def add_node(
        self,
        task: task_type_hint,
        upstreams: upstreams_type_hint = None,
        resource_queue: ResourceQueue | None = None,
        pip_extras: list[str] | None = None,
    ) -> None:
        """Add a node and edges from that node to the workflow."""
        if resource_queue is None:
            resource_queue = ResourceQueue.DEFAULT

        node = Node(
            workflow_name=self.workflow_name,
            workflow_version=self.workflow_version,
            workflow_package=self.workflow_package,
            task=task,
            resource_queue=resource_queue,
            upstreams=upstreams,
            pip_extras=pip_extras,
        )
        self.nodes.append(node)
        # confirm that the node can be properly added to a dag
        self._dag.add_task(node.operator)
        for upstream, downstream in node.dependencies:
            self._dag.set_dependency(upstream, downstream)

    def load(self) -> DAG:
        """Retrieve the native engine (airflow) workflow object."""
        return self._dag

    def export_dag(self, path: str | Path | None = None) -> Path:
        """Write a file representation of the workflow which can be run independently of the task dependencies."""
        path = path or "dags/"
        path = Path(path)
        path.mkdir(exist_ok=True)
        workflow_py = path / f"{self.dag_name}.py"

        with workflow_py.open(mode="w") as f:
            f.write(
                f"#  {self.workflow_name} workflow version {self.workflow_version} definition rendered for airflow scheduler\n"
            )
            f.write(self.workflow_imports)
            f.write("# Workflow\n")
            f.write(self.workflow_instantiation)
            f.write("    # Nodes\n")
            for n in self.nodes:
                operator = f"{n.task.__name__.lower()}_operator"
                f.write(f"    {operator} = {n.operator_definition}")
                f.write("\n")
            f.write("    # Edges\n")
            f.write(self.workflow_edges)
            f.write("\n")
        return workflow_py

    def export_notebook(self, path: str | Path | None = None):
        """Render the workflow as a jupyter notebook."""
        path = path or "notebooks/"
        path = Path(path)
        path.mkdir(exist_ok=True)
        notebook_ipynb = path / f"{self.dag_name}.ipynb"

        nb = nbf.v4.new_notebook()
        nb["cells"].append(nbf.v4.new_code_cell("recipe_run_id: int ="))
        for node in self.topological_sort():
            nb["cells"].append(nbf.v4.new_code_cell(node.notebook_cell))
        with open(notebook_ipynb, "w") as f:
            nbf.write(nb, f)
        return notebook_ipynb

    def topological_sort(self) -> [Node]:
        """Use a topological sort to find a valid linear order for task execution."""
        node_task_names = {node.task.__name__: node for node in self.nodes}
        node_upstream_tasks = {node.task: node.upstreams for node in self.nodes}
        ts = TopologicalSorter(graph=node_upstream_tasks)
        valid_node_order = [node_task_names[t.__name__] for t in ts.static_order()]
        return valid_node_order

    @property
    def workflow_imports(self) -> str:
        """Return the import statements for the workflow."""
        imports = [
            "from datetime import timedelta",
            "from functools import partial",
            "",
            "from airflow import DAG",
            "from airflow.operators.bash import BashOperator",
            "import pendulum",
            "",
            "from dkist_processing_core.failure_callback import chat_ops_notification",
            "",
            "",
        ]
        return "\n".join(imports)

    @property
    def workflow_instantiation(self) -> str:
        """Return the context manager instantiation of the workflow object."""
        return f"with {self.dag_definition} as d:\n    pass\n"

    @property
    def workflow_edges(self) -> str:
        """Return the edges between nodes for the workflow."""
        edges = []
        for n in self.nodes:
            for upstream, downstream in n.dependencies:
                edges.append(f"    d.set_dependency('{upstream}', '{downstream}')")
        return "\n".join(edges)

    def __repr__(self):
        """Detailed representation of the workflow."""
        return (
            f"Workflow("
            f"input_data={self.input_data}, "
            f"output_data={self.output_data}, "
            f"category={self.category}, "
            f"detail={self.detail}, "
            f"workflow_package={self.workflow_package}, "
            f"workflow_version={self.workflow_version}, "
            f")"
        )

    def __str__(self):
        """Representation of the workflow as a string."""
        return repr(self)
