# Contributing to my-jupyter-shared-drive

## Setting up a development environment

```console
micromamba create -n my-jupyter-shared-drive
micromamba activate my-jupyter-shared-drive
micromamba install pip nodejs
git clone https://github.com/davidbrochart/my-jupyter-shared-drive
cd my-jupyter-shared-drive
pip install -e .
pip install jupyterlab
jupyter labextension develop --overwrite .
```
