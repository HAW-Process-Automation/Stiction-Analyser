[![N|Solid](https://www.seeq.com/sites/default/files/seeq-logo-navbar-small.png)](https://www.seeq.com)

[![N|Scheme](StictionDetectionExample.png)](https://www.seeq.com)

----

**seeq-stictiondetection** is a Python module to detect oscillations and stiction patterns in control valves. The oscillation detection is able to detect and isolated the periods of time where the oscillation occurs. The stiction detector identifies if stiction is present within the further detected oscillating time periods. Both signals can be pushed back into the Seeq Workbench and further analysis (e.g. with the "Value Search" function). The module includes a user interface (UI) designed to interact with the Seeq server.

----

# User Guide

[**seeq-stictiondetection User Guide**](https://seeq12.github.io/seeq-stictiondetection/user_guide.html)
provides a more in-depth explanation of the algorithm behind the stiction analysis and how seeq-stictiondetection works. Examples of typical types
of analyses using **seeq-stictiondetection** can be found in the
section [Use Cases](https://seeq12.github.io/seeq-correlation/examples.html).

----

# Documentation

[Documentation for **seeq-stictiondetection**](https://seeq12.github.io/seeq-stictiondetection/documentation.html).

-----

# Installation

The backend of **seeq-stictiondetection** requires **Python 3.7** or later.

## Dependencies

See [`DocumentationStictionDetection.md`](https://github.com/Timothy716/seeq-stictiondetection/tree/master/TEST.md) file for a list of
dependencies and versions. Additionally, you will need to install the `seeq` module with the appropriate version that
matches your Seeq server. For more information on the `seeq` module see [seeq at pypi](https://pypi.org/project/seeq/)

## User Installation Requirements (Seeq Data Lab)

If you want to install **seeq-stictiondetection** as a Seeq Add-on Tool, you will need:

- Seeq Data Lab (>= R50.5.0, >=R51.1.0, or >=R52.1.0)
- `seeq` module whose version matches the Seeq server version
- Seeq administrator access
- Enable Add-on Tools in the Seeq server

## User Installation (Seeq Data Lab)

The latest build of the project can be found [here](https://pypi.seeq.com/) as a wheel file. The file is published as a
courtesy to the user, and it does not imply any obligation for support from the publisher. Contact
[Seeq](mailto:applied.research@seeq.com?subject=[seeq-stictiondetection]%20General%20Question) if you required credentials to
access the site.

1. Create a **new** Seeq Data Lab project and open the **Terminal** window
2. Run `pip install seeq-stictiondetection --extra-index-url https://pypi.seeq.com --trusted-host pypi.seeq.com`
3. Run `python -m seeq.addons.stictiondetection [--users <users_list> --groups <groups_list>]`

----

# Development

We welcome new contributors of all experience levels. The **Development Guide** has detailed information about
contributing code, documentation, tests, etc.

## Important links

* Official source code repo: https://github.com/seeq12/seeq-stictiondetection
* Issue tracker: https://github.com/seeq12/seeq-stictiondetection/issues

## Source code

You can get started by cloning the repository with the command:

```shell
git clone git@github.com:seeq12/seeq-stictiondetection.git
```

## Installation from source

For development work, it is highly recommended creating a python virtual environment and install the package in that
working environment. If you are not familiar with python virtual environments, you can take a
look [here](https://docs.python.org/3.8/tutorial/venv.html)

Once your virtual environment is activated, you can install **seeq-stictiondetection** from source with:

```shell
python setup.py install
```

## Testing

There are several types of testing available for **seeq-stictiondetection**

### Automatic Testing

After installation, you can launch the test suite from the root directory of the project (i.e. `seeq-stictiondetection `
directory). You will need to have pytest >= 5.0.1 installed

To run all tests:

```shell
pytest
```

There are several pytest markers set up in the project. You can find the description of the marks in the `pytest.ini`
file. You can use the `-m` flag to run only a subset of tests. For example, to run only the `backend` tests, you can
use:

```shell
pytest -m backend
```

The integration tests requires a connection to a Seeq server. The tests are configured to try to access a local Seeq
server with the data directory set up in `ProgramData/Seeq/data` of the local drive. However, you can set the
`seeq_url`, `credentials_file` configuration options in the `test_config.ini` file to run the integration tests on a
remote Seeq server, or change the local seeq data directory with `data_dir`.

*Note:* Remember that the `seeq` module version in your local environment should match the Seeq server version

### User Interface Testing

To test the UI, use the `developer_notebook.ipynb` in the `development` folder of the project. This notebook can also be
used while debugging from your IDE. You can also create a whl first, install it on your virtual environment, and then
run `developer_notebook.ipynb` notebook there.

----

# Changelog

The change log can be found [**here**](https://seeq12.github.io/seeq-stictiondetection/changelog.html)


----

# Support

Code related issues (e.g. bugs, feature requests) can be created in the
[issue tracker](https://github.com/seeq12/seeq-stictiondetection/issues)
Any other general comments or questions (non-code related) can be emailed to
[Seeq](mailto:applied.research@seeq.com?subject=[seeq-correlation]%20General%20Question)

Maintainer: Timothy Essinger


----

# Citation

Please cite this work as:

```shell
seeq-stictiondetection v0.0.1
Seeq Corporation, 2021
https://github.com/seeq12/seeq-stictiondetection
```






