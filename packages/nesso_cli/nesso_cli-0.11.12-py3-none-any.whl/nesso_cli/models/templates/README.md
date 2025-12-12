# {{ project_name }}

## Notice

The project is tested on Ubuntu 22.04 and Python 3.10.

## Prerequisites

- Python >= 3.9

**NOTE:** Remember to activate the virtual environment whenever working on the project (or use VSCode, which activates it automatically).

## Getting started
<!-- getting-started-begin -->
### Install prerequisites

The first step is to install all the prerequisites required by the project (such as database drivers or Python packages).

**NOTE:** You will be asked to provide your GitHub [Personal Access Token](https://docs.github.com/en/enterprise-server@3.6/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token). This token must have access to the [nesso-cli](https://github.com/dyvenia/nesso-cli) repository.

```bash
bash prepare.sh
```

### Activate the Python virtual environment

```bash
. .venv/bin/activate
```

### Install `nesso` CLI

```bash
pip3 install -qr requirements.txt
```

### Configure your database credentials

Run `nesso models init user` and follow the prompts.

## How to contribute models

Please refer to the [contributing guide](CONTRIBUTING.md) for specific instructions on how to contribute.

<!-- getting-started-end -->
