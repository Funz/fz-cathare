# fz-cathare

Cathare plugin for the [Funz](https://github.com/Funz/fz) framework - enabling parametric simulations with the CATHARE thermal-hydraulics code.

## Overview

This plugin provides integration between the Funz parametric computing framework and CATHARE (Code for Analysis of THermalhydraulics during an Accident of Reactor and safety Evaluation), a thermal-hydraulics simulation code.

## Structure

The plugin follows the new fz plugin structure:

- `.fz/models/Cathare.json` - Model definition with output parsing configuration
- `.fz/calculators/Localhost_Cathare.json` - Calculator configuration for local execution
- `tests/CNV22/` - Test case with sample input and output files

## Model Definition

The Cathare model uses the following configuration:

- **Variable prefix**: `$` (e.g., `$temperature`)
- **Formula prefix**: `@` (e.g., `@($temp + 273.15)`)
- **Delimiter**: `()` for variable and formula names
- **Comment line**: `*` at the start of a line

### Output Parsing

The plugin automatically parses CATHARE FORT07 output files to extract:

- **EVOLUTION** data sections containing time-series or spatial data
- **TIME_*** variables for time-dependent evolutions
- **Z_*** variables for space-dependent evolutions (using ZS or ZSW coordinates)

Each EVOLUTION section in the FORT07 file is parsed to extract:
- The variable name (e.g., ML, LIQMASS, PRESSURE)
- The x-axis values (TIME or Z coordinates)
- The corresponding data values

## Usage

### Basic Example

```python
import fz

# Define input variables
input_variables = {
    "param1": [1.0, 2.0, 3.0],
    "param2": 100
}

# Run parametric study
results = fz.fzr(
    "input_file",
    input_variables,
    model="Cathare",
    calculators="sh://cathare",
    results_dir="results"
)

# Access results
print(results)
```

### Output Variables

After running a simulation, you can access extracted variables such as:
- `ML`, `MV`, `MTOT` - Mass variables with corresponding `TIME_ML`, `TIME_MV`, `TIME_MTOT`
- `PRESSURE`, `TEMPERATURE` - Physical quantities
- Any other EVOLUTION data defined in your CATHARE output

## Installation

1. Install the Funz framework:
```bash
pip install fz
```

2. Clone this repository:
```bash
git clone https://github.com/Funz/fz-cathare.git
cd fz-cathare
```

3. Ensure CATHARE is installed and accessible in your PATH

## Testing

Test files are provided in `tests/CNV22/`:
- `input/` - Sample CATHARE input files
- `output/` - Sample CATHARE output files including FORT07

You can test the output parsing with:
```python
import fz

# Parse existing output directory
results = fz.fzo("tests/CNV22/output", model="Cathare")
print(results)
```

## Background

This plugin is a port of the original Java-based [plugin-cathare](https://github.com/Funz/plugin-cathare) to the new Python-based fz framework. The core functionality, especially the FORT07 output parsing logic from `CathareIOPlugin.java`, has been reimplemented in Python.

## License

This plugin inherits the LGPL license from the original plugin-cathare project.

## Links

- [CATHARE Website](http://www-cathare.cea.fr/)
- [Funz Framework](https://github.com/Funz/fz)
- [Original Plugin](https://github.com/Funz/plugin-cathare)