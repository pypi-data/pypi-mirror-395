Overview
========

The `dkist-processing-core` code repository provides an abstraction layer between the DKIST data
processing code, the workflow engine that supports it, and the observability infrastructure of the Data
Center.

.. image:: https://bitbucket.org/dkistdc/dkist-processing-core/raw/faf0c57f2155d03889fcd54bc1676a8a219f6ee3/docs/auto_proc_brick.png
  :width: 600
  :alt: Core, Common, and Instrument Brick Diagram

|

Four main entities implement the abstraction:

*Task* : The Task defines the interface used by a processing pipeline for a step in a workflow.
By conforming to this interface (i.e. subclassing), the processing pipelines can remain agnostic
of how the tasks will ultimately be run. The Task additionally implements some methods that should
be global for all DKIST processing tasks based on the infrastructure it will run on (e.g.
application performance monitoring infrastructure).

*Node* : The job of the Node is to translate a Task into code that can instantiate that task.
Instantiations of a Task can vary depending on the target environment, e.g. a virtual environment
with a BashOperator for the workflow engine vs. straight python for a notebook.

*Workflow* : The Workflow defines the interface used by the processing pipeline to chain tasks
together in a directed acyclic graph (DAG). The Workflow transforms this graph into the workflow
engine format by providing any wrapping boilerplate, task ordering, and selecting the appropriate
Node instantiation.

*Build Utils* : The Build Utils are the capstone layer which eases the transformation process
for multiple workflows at a time during a processing pipeline's build process.

The Workflow and Task are the primary objects used by client libraries.
