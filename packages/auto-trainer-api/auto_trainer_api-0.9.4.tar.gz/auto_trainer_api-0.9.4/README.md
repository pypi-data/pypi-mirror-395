# Autotrainer API: Python Integration

The python `auto-trainer-api` module is intended to provide an efficient means to emit information that
is needed for local or remote management and to receive commands from those sources.

The exposed API is intended to be agnostic to the underlying transport layer.  The current implementation uses
ZeroMQ for reasons described in the top-level README.

## Publishing
`python -m build`

`python -m twine upload dist/*` (requires PyPi API token)

## Installation
The package is published to the PyPi package index and can be installed with standard pip commands.

`pip install auto-trainer-api`
