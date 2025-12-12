# `invenio-typing-stubs`

This is a package that provides typing support for the InvenioRDM
source base. It is intended as a temporary solution until InvenioRDM
itself provides typing support.

As such, it is a collection of type stubs for the InvenioRDM
source base, as well as some utility functions to help with typing.

It must not contain any runtime code, it is intended to be used
only for type checking.

## Warning

These stubs were generated mostly automatically and only some have been
manually checked. They will surely contain some errors. Please report any
issues you find.

## Usage

Please install the package directly from github:

```bash
pip install git+https://github.com/oarepo/invenio-typing-stubs.git
```

If you add the dependency to your `pyproject.toml` built with hatchling, do it like:

```toml
[project.optional-dependencies]
dev = [
    "invenio-typing-stubs @ git+https://github.com/oarepo/invenio-typing-stubs.git",
]
```

## How it was generated

### Automatic generation

Copilot with GPT-5 was used to generate the stubs. The following
prompt was used:

```text
There is a agent_helper command that will give you work. Please call the command as 
`.venv/bin/python agent_helper.py invenio_communities`. 

The output of the command are the instructions that you should do. 
Read them carefully and execute them. 

After that, continue calling the agent and processing the instructions 
until it will tell you that all work has been done.
```

### Manual checks

Some manual checks were done to ensure the stubs are correct. Systemfields were
patched manually to ensure correct typing.

### Problems

Typing for SQL Alchemy mostly does not work with invenio_db.

### Final checks

Checked with

```bash
mypy --check-untyped-defs --ignore-missing-imports invenio_records_resources-stubs/
```

