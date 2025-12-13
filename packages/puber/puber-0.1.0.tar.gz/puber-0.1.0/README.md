# puber – Text tools for publishers

**puber** is a lightweight toolkit for text normalization and preparation for publishing workflows.

The project is designed as a growing set of utilities for working with human-oriented text data.

> At the moment, the package provides basic name normalization, but its functionality
  will be expanded with additional text processing tools in future releases.

---

## Installation

### Using pip

```bash
pip install --upgrade puber
```
For development:

```bash
pip install -e .
```

### Recommended for CLI use: pipx

If you primarily use `puber` as a command-line tool, it is best installed with **pipx**.  
This isolates the package in its own virtual environment and avoids polluting your system Python:

```bash
pipx install --upgrade puber
```

After installation it will be available globally:

```bash
puber --help
```

### Requirements

- Python **3.9+**
- macOS, Linux, or Windows

---

## Usage

### Command-line interface

Currently available commands:

```bash
# Normalize as personal name
puber norm -n "Татьяна М. Иванова" # -> Иванова Т.М.
```

---

### Python API

```python
from puber import norm_name

print(norm_name("Татьяна М. Иванова"))  # -> Иванова Т.М.
```

---

## Testing

The project includes an extensive automated test suite for text normalization.

Run tests from the project root:

```bash
pytest
```

For `src`-layout development:

```bash
pip install -e .
pytest
```

---

## License

MIT License  
(c) 2025 Timur Ulyahin  
https://github.com/ucomru

---

## Project Homepage

GitHub:  
https://github.com/ucomru/python-puber

PyPI:  
https://pypi.org/project/puber/
