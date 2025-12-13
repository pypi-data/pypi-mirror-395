# QuanTI-FRET

[Home](https://liphy-annuaire.univ-grenoble-alpes.fr/pages_personnelles/aurelie_dupont/quantifret/index_quantifret.html) |
[Documentation](https://liphy.gricad-pages.univ-grenoble-alpes.fr/quanti-fret/) |
[Source](https://gricad-gitlab.univ-grenoble-alpes.fr/liphy/quanti-fret) |
[PyPI](https://pypi.org/project/quanti-fret/) |
[Napari](https://napari-hub.org/plugins/quanti-fret.html)

`quanti-fret` is a Python tool that performs **QuanTI-FRET** calibration and
analysis from 3-channel movies

1. [Description](#description)
2. [Napari Plugin](#napari-plugin)
3. [Standalone GUI App](#standalone-gui-app)
4. [Standalone CLI App](#standalone-cli-app)
4. [Python Module](#python-module)
5. [Documentation](#documentation)
6. [For developpers](#for-developpers)

## Description

The **QuanTI-FRET** method proposes calibrating the instrument and the FRET pair
to simply calculate absolute FRET probabilities from a triplet of images
acquired under the same conditions and with the same FRET pair. All the
photophysical and instrumental factors are included in this calibration, leaving
the variability of the results to biological origins.

The `quanti-fret` package provides all the tools to perform first the
calibration, and then to make quantitative FRET measurement of your experiments,
using only your triplet images.

It can be used:
* As a [Napari](https://napari.org) plugin
* With the Standalone GUI app
* On the terminal with a CLI (Command Line Interface) app


## Napari Plugin

**QuanTI-FRET** was designed to be integrated into the
[Napari](https://napari.org) tool as a plugin.


### Installation

**QuanTI-FRET** is available in the
[Napari Hub](https://napari-hub.org/plugins/quanti-fret.html) under the name
`quanti-fret`.

To install it:
* Have a look [here](https://napari.org/stable/tutorials/fundamentals/installation.html#napari-installation)
  to install Napari
* Have a look [here](https://napari.org/stable/plugins/start_using_plugins/finding_and_installing_plugins.html#find-and-install-plugins)
  to install a plugin


### Getting Started

To open the plugin, go to the `Plugins` menu and click on `QuanTI-FRET (quanti-fret)`



## Standalone GUI App

You can also use the **QuanTI-FRET** software as a standalone GUI or CLI app
outside Napari.


### Installation

#### Set up your environment

It is good practice to set up a virtual environment and install the tool inside
your environment.

##### With Conda

```bash
conda create --name quantifret
conda activate quantifret
conda install pip
```

##### With Pyenv

```bash
pyenv virtualenv [PYTHON_VERSION>=3.10] quantifret
pyenv activate quantifret
pip install --upgrade pip
```

#### Install `Qt`

If you want to use the GUI application, you need to install `Qt`.

It is not in the defaults dependencies as the `quanti_fret` modules also comes
up with a CLI app, or can be imported directly inside your Python code. So we
don't want to penalize all the users by forcing a `Qt` dependency.

`quanti-fret` supports `Qt5` and `Qt6` using either `PyQt` or `PySide`

```bash
pip install [pyqt6 | pyqt5 | pyside6 | pyside5] # Choose one package
```

#### Install the module

Finally, you can install the `quanti_fret` module by running:
```bash
pip install quanti-fret
```

#### Upgrade the module

```bash
pip install quanti-fret --upgrade
```


### Getting Started

Run the following command inside your environement:`

```bash
quanti-fret-run
```


## Standalone CLI App

For automation purposes, or if you don't have access to a graphic server, you
can use the CLI app.

### Installation

Do all the steps of [the standalone GUI app installation](#standalone-gui-app)
except for the **Qt** part

### Getting Started

#### Generate your config files

You first need to generate one config file for the calibration phase, and one
for the fret phase:

```bash
quanti-fret-run generate_config calibration path/to/new/calibration.ini
quanti-fret-run generate_config fret path/to/new/fret.ini
```

You then need to modify them to fit your requirements (see the
[documentation](#documentation))

#### Run the calibration

```bash
quanti-fret-run cli calibration path/to/new/calibration.ini
```

#### Run the fret on the series
```bash
quanti-fret-run cli fret path/to/new/fret.ini
```



## Documentation

You can find the online documentation
[here](https://liphy.gricad-pages.univ-grenoble-alpes.fr/quanti-fret/)


## For developpers

Here are some indications dedicated to the developpers


### Poetry

`quanti-fret` is using poetry as a build system.

To install it, go to their [doc page](https://python-poetry.org/docs/)


### Clone the project

```bash
git clone https://gricad-gitlab.univ-grenoble-alpes.fr/liphy/quanti-fret.git
cd quanti-fret/
```


### Install QuanTI-FRET

```bash
poetry install
```


### Run the tests

```bash
pytest
flake8
mypy .
```
