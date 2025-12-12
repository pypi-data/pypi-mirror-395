# portableenv

`portableenv` is a Python CLI tool that allows you to create virtual environments using an embedded Python interpreter. This makes it easy to manage isolated Python environments without relying on the system-wide Python installation.

## Features

- **Seamless Virtual Environment Creation**: Creates virtual environments using the embedded Python interpreter, ensuring portability and isolation from system-wide installations.
- **Simple CLI Interface**: Provides a command-line interface similar to `virtualenv` for ease of use.

## Installation

Install `portableenv` via pip:

```bash
pip install portableenv
```

## Usage

### Create a Virtual Environment

To create a virtual environment using the embedded Python interpreter, use the following command:

```bash
python -m portableenv myenv
```

This will create a virtual environment named `myenv` using the embedded Python, Python 3.10.9 by default if not specified.

### Specifying a Different Python Version

You can specify a different Python version using the `-v` or `--version` option:

```bash
python -m portableenv myenv -v 3.11.5
```

This will download the embedded Python version 3.11.5 from python.org and use it to create the virtual environment.

The tool downloads the embedded Python distribution directly from python.org and configures it automatically. It also installs and updates pip to the latest version in both the embedded Python and the created virtual environment, ensuring you have the most up-to-date package manager without seeing upgrade notices when installing packages.

## Requirements

- Python 3.7 or higher
- `virtualenv` library (automatically installed with this package)
- Internet connection for the initial download of the embedded Python interpreter

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your changes.

## Author

- [AbdulRahim](https://github.com/abdulrahimpds)

## Links

- [GitHub Repository](https://github.com/abdulrahimpds/portableenv)
- [PyPI Package](https://pypi.org/project/portableenv)