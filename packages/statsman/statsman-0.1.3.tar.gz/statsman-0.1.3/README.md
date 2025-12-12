StatsMan is a terminal-based system monitoring tool that provides real-time system information using ASCII visualizations.

## Installation

### Using pipx

```bash
pipx install statsman
```

### Using pip

```bash
pip install statsman
```

## Usage

Run the tool:

```bash
statsman
```

### Options

```bash
statsman --help                     # Show help
statsman --refresh-rate 1.0         # Set refresh rate to 1 second
statsman --no-color                 # Disable color output
statsman --config ~/.statsman.yaml  # Use a custom configuration file
```

### Keyboard Controls

- `q` or `Ctrl+C`: Quit  
- `p`: Pause or resume updates  
- `c`: Sort processes by CPU usage  
- `m`: Sort processes by memory usage  
- `r`: Reset sorting  
- `↑` / `↓`: Navigate the process list  
- `Enter`: Terminate the selected process  

## Requirements

- Python 3.8 or higher  
- Currently statsman is built only for Linux, Windows support may be added in the future  

## Development

```bash
git clone https://github.com/ExilProductions/statsman.git
cd statsman

pip install -e ".[dev]"

python -m statsman
```

### Build wheel

To build a wheel distribution locally from the project root (where `pyproject.toml` lives):

```bash
# Install the build backend
python -m pip install build

# Build only the wheel
python -m build --wheel
```

The wheel file will be created in the `dist/` directory and can then be installed with:

```bash
pip install dist/statsman-<version>-py3-none-any.whl
```

## License

Released under the MIT License. See the [LICENSE](LICENSE) file for details.