# Nuttx-env

A Python library for creating and managing project environments for RTOS NuttX.

## Description

The 'nuttx-env' provides tools and utilities to set up development environments for NuttX RTOS projects.

## Features

- Automated NuttX project environment setup
- Development workflow automation
- Cross-platform support

## Installation

```bash
pip install nuttx-env
```

## Usage

```shell
# show help
nginx-env --help
```

## Development

Create environment for development

```shell
uv venv
# install libarary for dev
uv pip install -e .
```

Build library

```shell
python -m build
```

## License

MIT
