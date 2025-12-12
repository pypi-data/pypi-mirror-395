# db-contrib-tool

The `db-contrib-tool` - a collection of tooling to support repro environments.

## Description

The command line tool with various subcommands:
- `setup-repro-env`
  - [README.md](src/db_contrib_tool/setup_repro_env/README.md)
  - downloads and installs:
    - particular MongoDB versions
    - debug symbols
    - artifacts (including resmoke, python scripts etc)
    - python venv for resmoke, python scripts etc
- `setup-mongot-repro-env`
  - [README.md](src/db_contrib_tool/setup_mongot_repro_env/README.md)
  - Downloads and installs particular Mongot versions into install directory.
- `symbolize`
  - [README.md](src/db_contrib_tool/symbolizer/README.md)
  - Symbolizes stacktraces from recent `mongod` and `mongos` binaries compiled in Evergreen, including patch builds, mainline builds, and release/production builds.
  - Requires authenticating to an internal MongoDB symbol mapping service.

## Dependencies

- Python 3.9 or later (python3 from the [MongoDB Toolchain](https://github.com/10gen/toolchain-builder/blob/master/INSTALL.md) is highly recommended)

## Installation

Make sure [dependencies](#dependencies) are installed.
Use [pipx](https://pypa.github.io/pipx/) to install db-contrib-tool that will be available globally on your machine:

```bash
python3 -m pip install pipx
python3 -m pipx ensurepath
```

Installing db-contrib-tool:

```bash
python3 -m pipx install db-contrib-tool
```

Upgrading db-contrib-tool:

```bash
python3 -m pipx upgrade db-contrib-tool
```

In case of installation errors, some of them may be related to pipx and could be fixed by re-installing pipx.

Removing pipx completely (WARNING! This will delete everything that is installed and managed by pipx):

```bash
python3 -m pip uninstall pipx
rm -rf ~/.local/pipx  # in case you're using the default pipx home directory
```

Now you can try to install again from scratch.

## Usage

Print out help message:

```bash
db-contrib-tool --help
```

Download and install the v8.0 mongo binary:
```sh
db-contrib-tool setup-repro-env 8.0
```

Download other accompanying artifacts with flags:
```sh
db-contrib-tool setup-repro-env 8.0 \
  --downloadSymbols \
  --downloadArtifacts \
  --downloadPythonVenv
```

Download latest binary from the 10gen/mongo master branch:
```sh
db-contrib-tool setup-repro-env master
```

There are more ways to specify binary versions - see [setup_repro_env/README.md](src/db_contrib_tool/setup_repro_env/README.md).

# Contributing

See [./CONTRIBUTING.md](./CONTRIBUTING.md) on details for development on this project.
