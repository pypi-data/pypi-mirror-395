# Coauthor AI Agent

[![Documentation Status](https://readthedocs.org/projects/coauthor/badge/?version=latest)](https://coauthor.readthedocs.io/en/latest/?badge=latest)
[![pipeline status](https://gitlab.com/c2platform/c2/coauthor/badges/master/pipeline.svg)](https://gitlab.com/c2platform/c2/coauthor/-/commits/master)
[![coverage report](https://gitlab.com/c2platform/c2/coauthor/badges/master/coverage.svg)](https://gitlab.com/c2platform/c2/coauthor/-/commits/master)
[![PyPI version](https://img.shields.io/pypi/v/coauthor)](https://pypi.org/project/coauthor)
[![Pyversions](https://img.shields.io/pypi/pyversions/coauthor.svg?style=flat-square)](https://pypi.org/project/coauthor/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<!-- start mini-description -->

Coauthor is a versatile AI agent designed to seamlessly integrate into any
project without being restricted to a particular tool or IDE. It functions as a
co-author, operating in the background to monitor files and respond to
instructions for collaboratively producing documentation, code, configuration,
and more.

The agent is powered by a simple task engine that allows you to define
workflows—collections of tasks that are executed in sequence when certain
conditions, such as file or directory changes, are met. This task engine is
enhanced by the Jinja templating engine, providing extensive control over system
and user prompts.

<!-- end mini-description -->

## Installing

:start-after: <!-- start installing -->

To install Coauthor run the following command:

```bash
pip install coauthor
```

<!-- end installing -->

## Configuration `.coauthor.yml`

To do anything meaningful with coauthor you have to create a configuration file
`.coauthor.yml`. For example in the root of a folder that contains Obsidian markdown
files. Refer to the
[documentation website](https://coauthor.readthedocs.io/en/latest/users/configuration_file.html)
for more information.

## Command line usage

Create a file `.coauthor.yml` in the root of your project, for example in a
Obsidian project where all my Obsidian vaults are in directory `vaults`:

<!-- start cli-usage -->

Start Coauthor run the following commands:

```bash
export OPENAI_API_KEY=<you api key>
export OPENAI_API_URL=https://openrouter.ai/api/v1
coauthor --watch
```

To see command line options, run `coauthor --help`.

<!-- end cli-usage -->

## Contributing

This project welcomes contributions and suggestions. For details, visit the
repository's
[Contributor Page](https://coauthor.readthedocs.io/en/latest/contributors/contributing.html).
