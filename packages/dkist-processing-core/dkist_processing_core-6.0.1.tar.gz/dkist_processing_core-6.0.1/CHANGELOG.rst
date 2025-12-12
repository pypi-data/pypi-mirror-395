v6.0.1 (2025-12-03)
===================

Misc
----

- Add a dkist.root attribute to the top level span instrumented by dkist-processing-core to aid in trace discovery when auto-instrumentation takes over the root span. (`#57 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/57>`__)
- Update the minimum dkist-service-configuration version to force additional telemetry discovery metadata into downstream processing pipelines. (`#57 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/57>`__)
- Add telemetry attributes for resource allocation metadata to aid in discovery/analysis of traces and metrics. (`#58 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/58>`__)


v6.0.0 (2025-09-26)
===================

Misc
----

- Swap out Elastic APM for OpenTelemetry tracing and metrics. (`#56 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/56>`__)


v5.2.1 (2025-09-08)
===================

Misc
----

- Update ReadTheDocs configuration to use python 3.12.


v5.2.0 (2025-09-08)
===================

Misc
----

- Update pre-commit hook versions and replace python-reorder-imports with isort. (`#54 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/54>`__)
- Update dependencies to airflow 2.11.0 and limit to python >=3.12. (`#55 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/55>`__)


v5.1.1 (2025-05-22)
===================

Bugfixes
--------

- Don't use `--system-site-packages` in pip install command for task dependencies. (`#53 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/53>`__)


Misc
----

- Add coverage badge to README.rst. (`#51 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/51>`__)
- Add missing build dependency specifications. (`#52 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/52>`__)


v5.1.0 (2025-02-24)
===================

Misc
----

- Update apache-airflow to 2.10.5. (`#50 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/50>`__)


v5.0.0 (2025-02-14)
===================

Features
--------

- Instrument python packages are now installed using their "frozen" pip extra, which contains a complete set of frozen dependencies.
  This ensures the environment is exactly the same for a given version of an instrument repo. (`#48 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/48>`__)


Misc
----

- Update bitbucket pipelines to use common scripts for checking for changelog snippets and verifying doc builds. (`#47 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/47>`__)
- Update Bitbucket pipelines to use execute script for standard steps. (`#49 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/49>`__)


v4.3.0 (2025-01-08)
===================

Misc
----

- Make and publish wheels at code push in build pipeline (`#43 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/43>`__)
- Switch from setup.cfg to pyproject.toml for build configuration (`#43 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/43>`__)
- Update Bitbucket pipelines to use standardized lint and scan steps. (`#45 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/45>`__)
- Upgrade apache-airflow to 2.10.4. (`#46 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/46>`__)


Documentation
-------------

- Change the documentation landing page to focus more on users and less on developers. (`#44 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/44>`__)


v4.2.1 (2024-09-27)
===================

Misc
----

- Specify an output processor for the airflow BashOperator to fix a bug in documentation builds. (`#42 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/42>`__)


v4.2.0 (2024-09-27)
===================

Misc
----

- Fixing deprecation warnings in pkg_resources. (`#39 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/39>`__)
- Utility for generating the name of a workflow is part of the public API. (`#40 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/40>`__)
- Upgrade to airflow 2.10.2. (`#41 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/41>`__)


v4.1.0 (2024-07-01)
===================

Misc
----

- Add utility for generating the name of a workflow. (`#35 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/35>`__)
- Update the instructions for development to include the dependency on rabbitmq and docker. (`#36 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/36>`__)
- Make private methods public when we want them to show up in the ReadTheDocs documentation. (`#37 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/37>`__)
- Upgrade airflow to version 2.9.2. (`#38 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/38>`__)


v4.0.0 (2024-06-03)
===================

Bugfixes
--------

- Use --user option to upgrade pip before virtual environment creation. (`#33 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/33>`__)


Misc
----

- Upgrade airflow to 2.9.1 which includes the dependency on pydantic 2 and consequently a few other libraries that needed upgrading for the same pydantic 2 dependency. (`#34 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/34>`__)


v3.1.0 (2024-04-02)
===================

Features
--------

- Add a 'rollback' method to the Task API for removing changes to persistent stores performed by the task. (`#32 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/32>`__)


v3.0.1 (2023-12-20)
===================

Features
--------

- Remove the build extra because there isn't enough separation of deps yet. (`#29 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/29>`__)


v3.0.0 (2023-12-20)
===================

Features
--------

- Add utility to create a Jupyter notebook rendering of a workflow for manual execution. (`#26 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/26>`__)
- Enable the generation of Dockerfiles for building the manual processing worker services. (`#26 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/26>`__)


Misc
----

- Support specifying pip extras for individual nodes in a workflow. (`#23 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/23>`__)
- Developer documentation enhancements. (`#27 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/27>`__)


v2.1.2 (2023-11-24)
===================

Misc
----

- Update usages of deprecated Airflow APIs to use the suggested replacements. (`#24 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/24>`__)
- Update airflow dependency to 2.7.3. (`#25 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/25>`__)


v2.1.0 (2023-11-13)
===================

Features
--------

- Support assigning a resource queue to a node in a workflow when adding it to the workflow. (`#22 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/22>`__)


v2.0.2 (2023-07-11)
===================

Misc
----

- Update airflow dependency to 2.6.3 (`#21 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/21>`__)


v2.0.1 (2023-06-28)
===================

Bugfixes
--------

- Update MAXIMUM_ALLOWED_WORKFLOW_NAME_LENGTH to be consistent with database (100 characters). (`#19 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/19>`__)


Misc
----

- Update airflow dependency to 2.6.2 and use python 3.11 (`#20 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/20>`__)
- Use python 3.11 in ReadTheDocs builds

v1.4.0 (2023-05-05)
===================

Misc
----

- Update pip before use (`#17 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/17>`__)
- Move to airflow 2.6.0 (`#18 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/18>`__)


v1.3.0 (2023-02-17)
===================

Misc
----

- Update Airflow to v2.5.1


v1.2.0 (2022-11-15)
===================

Misc
----

- Update airflow dependency to include optional celery dependencies. (`#16 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/16>`__)


Documentation
-------------

- Add changelog to RTD left hand TOC to include rendered changelog in documentation build. (`#16 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/16>`__)

v1.1.2 (2022-11-02)
===================

Misc
----

- Add additional logging of container allocation information to the task startup logs to shorten investigations that may be allocation specific. (`#15 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/15>`__)


v1.1.1 (2022-10-20)
===================

Misc
----

- Make python 3.10 the minimum supported version (`#14 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/14>`__)


v1.1.0 (2022-10-10)
===================

Features
--------

- Update airflow version from 2.2.4 to 2.4.1. Details can be found here: https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html (`#13 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/13>`__)


v1.0.1 (2022-09-28)
===================

Features
--------

- Implement static method to create workflow name from constituent parts.
  This will be used by the calibration_workflow_name pre-commit hook. (`#12 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/12>`__)


v1.0.0 (2022-08-08)
===================

Removals
--------

- Updated the workflow naming API with breaking changes which do not support the old implementation. (`#11 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/11>`__)


Documentation
-------------

- Add CHANGELOG and towncrier machinery (`#10 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/10>`__)


v0.3.6 (2022-04-19)
===================

Misc
----

- Removing pinning of `markupsafe` version (related to airflow version 2.2.4)

v0.3.5 (2022-04-19)
===================

Misc
----

- Update airflow version to 2.2.4

v0.3.4 (2022-04-19)
===================

Features
--------

- Allow arbitrary tags on DAG names in Airflow (`#9 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/9>`__)


v0.3.3 (2022-03-11)
===================

Features
--------

- Update pip prior to installing pipeline into virtual env (`#8 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/8>`__)


v0.3.2 (2022-03-11)
===================

Documentation
-------------

- Update docstrings to comply with pydocstyle


v0.3.1 (2022-02-22)
===================

Bugfixes
--------

- Adding dependency fix due to Airflow pinning flask

v0.3.0 (2022-02-17)
===================

Misc
----

- Label `run()` apm spans as type "core" (`#6 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/6>`__)
- Update python and airflow to 3.9 and 2.2.3, respectively (`#7 <https://bitbucket.org/dkistdc/dkist-processing-core/pull-requests/7>`__)
