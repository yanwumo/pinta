# Pinta: Job management on GPU clusters 🍺

## Installation

To install the command-line client:

``` bash
pip3 install pinta
```

To install the backend API server:

``` bash
pip3 install pinta-api
```

Pinta requires Python 3.8.


## Development

To start contributing to Pinta:

``` bash
git clone git@github.com:qed-usc/pinta.git
cd pinta
poetry install
```

You can run Pinta from the local directory with `poetry run pinta` (or by first
starting `poetry shell` and then `pinta`).

To run the tests: `poetry run pytest`.

To check the documentation: `poetry run mkdocs serve`.

To deploy the documentation: `poetry run mkdocs gh-deploy`.
