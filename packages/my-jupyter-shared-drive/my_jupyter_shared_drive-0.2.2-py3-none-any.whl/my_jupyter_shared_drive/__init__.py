# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import importlib.metadata


try:
    __version__ = importlib.metadata.version("my-jupyter-shared-drive")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": "@jupyter/my-shared-docprovider-extension"}]
