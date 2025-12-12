"""Configuration file for the Sphinx documentation builder."""

# -- stdlib imports ------------------------------------------------------------
import importlib
import sys
import warnings
from importlib.metadata import distribution

from dkist_sphinx_theme.conf import *
from packaging.version import Version

# Need a name for the overall repo
# __name__ where this code executes is "builtins" so that is no help
repo_name = "dkist-processing-core"
package_name = repo_name.replace("-", "_")

dist = distribution(package_name)
package = importlib.import_module(package_name)

# -- Check for docs dependencies ----------------------------------------------------
missing_requirements = missing_dependencies_by_extra(package_name, extras=["docs"])
if missing_requirements["docs"]:
    print(
        f"The {' '.join(missing_requirements['docs'])} package(s) could not be found and "
        "is needed to build the documentation, please install the 'docs' requirements."
    )
    sys.exit(1)

# auto api parameters that cannot be moved into the theme:
autoapi_dirs = [Path(package.__file__).parent]
# Uncomment this for debugging
autoapi_keep_files = True

# -- Options for intersphinx extension -----------------------------------------
intersphinx_mapping = {
    # Official Python docs
    "python": (
        "https://docs.python.org/3/",
        "https://docs.python.org/3/objects.inv",
    ),
    # OpenTelemetry (Python)
    "opentelemetry": (
        "https://opentelemetry-python.readthedocs.io/en/stable/",
        "https://opentelemetry-python.readthedocs.io/en/stable/objects.inv",
    ),
}
# Remaining sphinx settings are in dkist-sphinx-theme conf.py

# -- Project information -------------------------------------------------------
project = "DKIST-PROCESSING-CORE"

# The full version, including alpha/beta/rc tags
dkist_version = Version(dist.version)
is_release = not (dkist_version.is_prerelease or dkist_version.is_devrelease)
# We want to ignore all warnings in a release version.
if is_release:
    warnings.simplefilter("ignore")
