# VGS CLI

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/verygoodsecurity/vgs-cli/tree/master.svg?style=svg&circle-token=6d4536882cc1d60a7ecf15cf4b4c93286abff2d8)](https://dl.circleci.com/status-badge/redirect/gh/verygoodsecurity/vgs-cli/tree/master)

Command Line Tool for programmatic configurations on VGS.

[Official Documentation](https://www.verygoodsecurity.com/docs/vgs-cli/getting-started)

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
  - [PyPI](#pypi)
- [Run](#run)
- [Running in Docker](#running-in-docker)
- [Commands](#commands)
- [Automation with VGS CLI](#automation-with-vgs-cli)
- [Sphinx Documentation](#sphinx-documentation)
- [Plugins Development](#plugins-development)

## Requirements
[Python 3](https://www.python.org/downloads/) or [Docker](https://docs.docker.com/get-docker/).

## Installation

### PyPI
Install the latest version from [PyPI](https://pypi.org/project/vgs-cli/):
```
pip install vgs-cli
```

## Run

Verify your installation by running:
```
vgs --version
```

## Running in Docker

Check our [official documentation](https://www.verygoodsecurity.com/docs/vgs-cli/docker).

## Commands

- [`help`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#exploring-the-cli)
- [`login`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#login)
- [`logout`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#logout)
- [`routes get`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#get)
- [`routes apply`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#apply)
- [`logs access`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#access)
- [`access-credentials get`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#get)
- [`access-credentials generate`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#generate)
- [`organizations get`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#get)
- [`vaults get`](https://www.verygoodsecurity.com/docs/vgs-cli/commands#get)

## Automation with VGS CLI

If you want to use the VGS CLI for automation you might be interested in creating a [service account](https://www.verygoodsecurity.com/docs/vgs-cli/service-account).

## Plugins Development

See [Click - Developing Plugins](https://github.com/click-contrib/click-plugins#developing-plugins).

In order to develop a plugin you need to register your commands to an entrypoint in `setup.py`.

Supported entrypoints:

- `vgs.plugins` - for extending `vgs` with sub-commands
- `vgs.get.plugins` - for extending `vgs get` with sub-commands
- `vgs.apply.plugins` - for extending `vgs apply` with sub-commands
- `vgs.logs.plugins` - for extending `vgs logs` with sub-commands

Example:
```python
entry_points='''
    [vgs.plugins]
    activate=vgscliplugin.myplugin:new_command

    [vgs.get.plugins]
    preferences=vgscliplugin.myplugin:new_get_command
'''
```

### Plugin catalog
- [vgs-cli-admin-plugin](https://github.com/verygoodsecurity/vgs-cli-admin-plugin)