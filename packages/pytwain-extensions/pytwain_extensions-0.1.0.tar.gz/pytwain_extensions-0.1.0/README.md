# Twain Extensions

Twain Extensions is a Python library designed to enhance usability of the [pytwain](https://pypi.org/project/pytwain/) library with a pytonic design layered on top of the existing functionality.

## Features

- **Capability Registries**: Predefined registries for audio, image, and general capabilities including documentation from the [TWAIN specification](https://twain.org/wp-content/uploads/2021/11/TWAIN-2.5-Specification.pdf).
- **Dynamic Code Generation**: Can generate a pydantic model for the configuration of a given scanner using Jinja2 templates.
- **Enhanced Data Types**: Translates TWAIN specific enums and frames into pythonicly typed variables.

## Groups
The library offers grouped installation of dependencies for different use cases:
- `twain_extensions`: Installs the core library with enums and registries. No additional dependencies.
- `twain_extensions[dev]`: Includes all development dependencies such as testing and linting tools.
- `twain_extensions[generate]`: Includes dependencies required for code generation features.

## Installation

To install the required dependencies, I recommend using [uv](https://uv.sh/).

```bash
uv sync --all-groups
```

## Usage

### Generating Scanner Models

You can generate a Python model for a scanner configuration using the `generate_scanner_model` function:

```python
from twain_extensions.generate.generate import generate_scanner_model

source = twain.Source("Your Scanner Name")
generate_scanner_model(source, "output_file.py")
```

### Capability Registries

The library includes predefined registries for various TWAIN capabilities:

- `AUDIO_CAP_REGISTRY`
- `IMAGE_CAP_REGISTRY`
- `GENERAL_CAP_REGISTRY`


## Project Structure

```
.
├── src/
│   ├── twain_extensions/
│   │   ├── enums.py
│   │   ├── frame.py
│   │   ├── generate/
│   │   │   ├── generate.py
│   │   │   ├── template.py
│   │   ├── registries/
│   │   │   ├── audio_capabilities.py
│   │   │   ├── capability.py
│   │   │   ├── general_capabilities.py
│   │   │   ├── image_capabilities.py
├── tests/
│   ├── test_registries.py
│   ├── test_registry_entries.py
```

## Development

### Running Tests

To run the tests, use:

```bash
pytest
```

### Linting

This project uses Ruff for linting. To check for linting errors, run:

```bash
ruff check .
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgments & Copyrights

This software is an implementation of the TWAIN specification.

* TWAIN (Classic) Specification: © 1991-2025 TWAIN Working Group. All rights reserved.

* Portions of the documentation strings in this library are quoted directly from the TWAIN Specification to assist developers. These descriptions remain the intellectual property of the TWAIN Working Group.

* For more information, visit twain.org.

## Contact

For any questions or feedback, please contact Jonathan Costa at jonathanleonhard.costa@gmail.com.
