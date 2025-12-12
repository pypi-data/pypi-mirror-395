"""Example invalid workflow for"""

from dkist_processing_core import Workflow
from dkist_processing_core.tests.task_example import Task

category_a = Workflow(
    input_data="test-data",
    output_data="invalid",
    category="A",
    workflow_package=__package__,
)
category_a.add_node(task=Task, upstreams=None)


category_b = Workflow(
    input_data="test-data",
    output_data="invalid",
    category="B",
    workflow_package=__package__,
)
category_b.add_node(task=Task, upstreams=None)
