# Spheronizator
Spheronizator is a Python research utility designed to voxelize protein structural data from existing PDB files for use in machine learning training sets. The utility is intended to be a part of your data processing pipeline, with an interface that is convenient to use with [IPython](https://ipython.org/), [Jupyter](https://jupyter.org/), or similar. Please see the [detailed documentation](https://spheronizator.readthedocs.io/) for more information, usage, and examples.

## Documentation
Detailed documentation for the project can be found here:
[https://spheronizator.readthedocs.io/](https://spheronizator.readthedocs.io/)

Documentation for the project is written in Markdown, rendered to a static site with [mdBook](https://rust-lang.github.io/mdBook/), and hosted by [Read the Docs](https://readthedocs.org/).

## Installation
The precompiled package is hosted on [PyPI](https://pypi.org/project/spheronizator/) and can be easily installed with pip:

```
pip install spheronizator
``` 

### Using a Conda Environment
If you prefer to install the package into a Conda environment, you can use configuration from the repository.

First download the configuration:
```
curl -L -o spheronizator_env.yml https://raw.githubusercontent.com/mattlrich/spheronizator/refs/heads/main/spheronizator_env.yml
```

Now create a Conda environment using the configuration:
```
conda env create -f spheronizator_env.yml
```
```
conda activate spheronizator
```

You can now install the package into the environment with pip:
```
pip install spheronizator
``` 

## Development
Packaging and building of the project is handled by [Poetry](https://python-poetry.org/docs/).

To install the development version, first install Poetry:

```
pipx install poetry
```

then clone the repository:

```
git clone git@github.com:mattlrich/spheronizator.git
```

then install the package in development mode to a virtual environment:

```
poetry install
```

You can build the source and wheels archives with:

```
poetry build
```

## Bugs and Issues
If you encounter any issues with the package, please report them through the [GitHub Issue Tracker](https://github.com/mattlrich/spheronizator/issues).

## Contributing
The project is happy to accept contibutions and enhancements. All contributions are to be made through GitHub pull requests. See [CONTRIBUTING](CONTRIBUTING.md) for more information.

## Contact
- **Matthew Richardson** — richardson.m@ufl.edu
- **Jose Cleydson** — jferreiradasilva@ufl.edu
- **José Cediel-Becerra** — jcedielbecerra@ufl.edu
- **Raquel Dias** — raquel.dias@ufl.edu

## License
Spheronizator is licensed under the [BSD 3-Clause License](https://choosealicense.com/licenses/bsd-3-clause/). Please see [LICENSE](LICENSE) for more information.
