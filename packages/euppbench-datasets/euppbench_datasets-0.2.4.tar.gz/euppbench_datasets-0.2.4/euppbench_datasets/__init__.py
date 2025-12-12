import importlib.metadata
import importlib.resources as pkg_resources

import intake

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


def open_catalog():
    # Use pkg_resources to access the catalog.yaml file
    # This is a more robust way to access package resources
    # and works well with both local and installed packages.
    # The path is relative to the package name.
    # The catalog.yaml file should be in the euppbench_datasets/catalog directory.
    with pkg_resources.path("euppbench_datasets.catalog", "catalog.yml") as catalog_path:
        return intake.open_catalog(str(catalog_path))
