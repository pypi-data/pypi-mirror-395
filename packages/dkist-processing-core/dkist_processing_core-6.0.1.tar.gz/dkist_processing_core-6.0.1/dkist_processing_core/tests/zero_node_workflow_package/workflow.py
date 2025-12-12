"""Workflow containing zero nodes."""

from dkist_processing_core import Workflow

zero_node_workflow = Workflow(
    input_data="test-data",
    output_data="zero-node",
    category="core",
    workflow_package=__package__,
)
