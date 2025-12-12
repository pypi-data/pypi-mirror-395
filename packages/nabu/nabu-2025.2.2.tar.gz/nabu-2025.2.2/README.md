# Nabu

ESRF tomography processing software.

## Installation

To install the development version:

```bash
pip install [--user] git+https://gitlab.esrf.fr/tomotools/nabu.git
```
To install the stable version:

```bash
pip install [--user] nabu
```

## Usage

Nabu can be used in several ways:
  - As a Python library, by features like `Backprojector`, `FlatField`, etc
  - As a standalone application with the command line interface
  - From Tomwer ([https://gitlab.esrf.fr/tomotools/tomwer/](https://gitlab.esrf.fr/tomotools/tomwer/))

To get quickly started, launch:
```bash
nabu-config 
```
Edit the generated configuration file (`nabu.conf`). Then:

```bash
nabu nabu.conf --slice 500-600
```

will reconstruct the slices 500 to 600, with processing steps depending on `nabu.conf` contents.

## Documentation

The documentation can be found on the silx.org page ([https://www.silx.org/pub/nabu/doc](http://www.silx.org/pub/nabu/doc)).

The latest documentation built by continuous integration can be found here: [https://tomotools.gitlab-pages.esrf.fr/nabu/](https://tomotools.gitlab-pages.esrf.fr/nabu/)

## Running the tests

Once nabu is installed, running

```bash
nabu-test
```
will execute all the tests. You can also specify specific module(s) to test, for example:
```bash
nabu-test preproc misc
```
You can also provide more `pytest` options, for example increase verbosity with `-v`, exit at the first fail with `-x`, etc. Use `nabu-test --help` for displaying the complete options list.



## Nabu - what's in a name ?

Nabu was the Mesopotamian god of literacy, rational arts, scribes and wisdom.
