# scaffoldry 

![Version](https://img.shields.io/badge/version-0.0.1a-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10-yellow)

## Description

A package to perform a generic project with multiple languages and frameworks.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [Tests](#tests)
- [FAQ](#faq)
- [License](#license)
- [Contact](#contact)

  
## Installation
Install via pip:

```bash
pip install scaffoldry --pre
```

## Usage

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `generate`: Generate all the content related with the...
* `create-template`: Create a template in json in order to...

## `generate`

Generate all the content related with the input file provided

**Usage**:

```console
$ generate [OPTIONS] PATH_DEFINITION PATH_LOCATION
```

**Arguments**:

* `PATH_DEFINITION`: Path with the definition file  [required]
* `PATH_LOCATION`: Output root path in which the project is generated  [required]

**Options**:

* `--help`: Show this message and exit.

## `create-template`

Create a template in json in order to modify it.

**Usage**:

```console
$ create-template [OPTIONS] PATH_LOC
```

**Arguments**:

* `PATH_LOC`: Path to store the template  [required]

**Options**:

* `--help`: Show this message and exit.

## Features

Generation of base projects in python

## Contributing

At a glance:  
- Create an issue inside the project to raise a bug or suggest an improvement
- Recomendation: If you wait until I answer you can ensure that the issue will be accepted
- Create a branch referring with this issue to work with the code.
- Open a MR

## FAQ

- Why not use alternatives like Cookiecutter?
This package supports multiple languages and frameworks, making it easy to switch while keeping a consistent structure.

- Why does it seem less flexible?
It favors clear, well-defined structures to simplify code generation. Flexibility is reduced, but output is predictable and reliable.


## Licence

MIT

## Contact

You can contact with the user of this repo.  
