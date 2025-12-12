# quart-shell-ipython

generated from flask-shell-ipython

Start quart shell with ipython, if it installed

## Features

- Drop-in replacement for the default Quart shell command
- Full IPython integration with enhanced REPL features
- Python 3.7+ support, including Python 3.13
- Compatible with Python 3.13's improved asyncio event loop handling

## Installation

```bash
pip install quart-shell-ipython
```

## Usage

Once installed, the package automatically registers a `shell` command
with your Quart application. Simply run:

```bash
quart shell
```

You can pass any IPython arguments:

```bash
quart shell --no-banner --quick
```

## Python 3.13 Compatibility

This package has been updated to work seamlessly with Python 3.13's
stricter asyncio event loop management. The shell command properly
handles event loop creation and management to ensure compatibility
across all supported Python versions.
