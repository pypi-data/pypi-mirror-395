# Quick Start

Ecosystem Plugin for Sonic support in Ape

## Dependencies

- [python3](https://www.python.org/downloads) version 3.9 up to 3.12.

## Installation

### via `ape`

You can install this plugin using `ape`:

```bash
ape plugins install sonic
```

or via config file:

```yaml
# ape-config.yaml
plugins:
  - name: sonic
```

### via `pip`

You can install the latest release via [`pip`](https://pypi.org/project/pip/):

```bash
pip install ape-sonic
```

### via `setuptools`

You can clone the repository and use [`setuptools`](https://github.com/pypa/setuptools) for the most up-to-date version:

```bash
git clone https://github.com/ApeWorX/ape-sonic.git
cd ape-sonic
python3 setup.py install
```

## Quick Usage

Installing this plugin adds support for the Sonic ecosystem:

```bash
ape console --network sonic:mainnet
```
