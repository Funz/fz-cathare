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

### Quick Example: Parse Existing Output

```python
import fz

# Parse CATHARE output directory
results = fz.fzo("path/to/output/directory", model="Cathare")

# Access parsed variables (all in the '*' column as a dictionary)
output_vars = results['*'].iloc[0]

# Display available variables
for var_name, values in output_vars.items():
    print(f"{var_name}: {len(values)} data points")

# Access specific variables
time_values = output_vars['TIME_ML']
mass_values = output_vars['ML']
```

### Parametric Study Example

```python
import fz

# Create input template with variables
# Your CATHARE input file should contain variables like:
# TEMP = $temperature
# PRESS = $pressure

# Define parameter values
input_variables = {
    "temperature": [300, 350, 400],  # 3 temperatures
    "pressure": [1e5, 2e5, 3e5]       # 3 pressures
}

# Run all combinations (3 × 3 = 9 cases)
results = fz.fzr(
    "cathare_input.dat",
    input_variables,
    model="Cathare",
    calculators="sh://cathare",
    results_dir="results"
)

# Results DataFrame includes all input variables and parsed outputs
print(results)
```

### Three-Step Workflow

The fz framework provides three separate functions for more control:

```python
import fz

# 1. Detect variables in input file
variables = fz.fzi("input.dat", model="Cathare")
print(f"Found variables: {list(variables.keys())}")

# 2. Compile input files with parameter values
fz.fzc(
    "input.dat",
    {"temperature": [300, 350], "pressure": [1e5, 2e5]},
    model="Cathare",
    output_dir="compiled_inputs"
)

# 3. Parse output files
results = fz.fzo("output_directory", model="Cathare")
```

### Output Variables

After running a simulation, you can access extracted variables such as:
- `ML`, `MV`, `MTOT` - Mass variables with corresponding `TIME_ML`, `TIME_MV`, `TIME_MTOT`
- `LIQMASS`, `STEAMASS` - Liquid and steam mass
- `PRESSURE`, `TEMPERATURE` - Physical quantities at different locations
- `QL`, `QV` - Liquid and vapor flow rates
- Any other EVOLUTION data defined in your CATHARE output

The plugin automatically extracts:
- **TIME_*** - Time-dependent evolution data (x-axis in seconds)
- **Z_*** - Space-dependent evolution data (x-axis in meters, for ZS/ZSW coordinates)

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

## Examples

Several example scripts are provided to demonstrate the plugin:

### 1. Basic Output Parsing (`example.py`)

Shows how to parse CATHARE output files:
```bash
python3 example.py
```

### 2. Parametric Study Workflow (`example_parametric_study.py`)

Demonstrates the complete workflow for parametric studies:
```bash
python3 example_parametric_study.py
```

This example shows:
- Variable detection in input files
- Input compilation with parameter grids
- Output parsing and data extraction

### 3. Example Input Template (`tests/example_parametric.txt`)

A sample CATHARE input file showing how to use variables:
```
* Temperature parameter
TEMP = $temperature

* Pressure parameter  
PRESS = $pressure

* Calculated parameter using formula
DENSITY = @($pressure / (287.0 * $temperature))
```

## Testing

Test files are provided in `tests/CNV22/`:
- `input/` - Sample CATHARE input files
- `output/` - Sample CATHARE output files including FORT07

### Run Tests

```bash
# Test output parsing accuracy
python3 tests/test_output_parsing.py

# Parse existing output directory
python3 -c "import fz; print(fz.fzo('tests/CNV22/output', model='Cathare'))"
```

## Background

This plugin is a port of the original Java-based [plugin-cathare](https://github.com/Funz/plugin-cathare) to the new Python-based fz framework. The core functionality, especially the FORT07 output parsing logic from `CathareIOPlugin.java`, has been reimplemented in Python.

## License

This plugin inherits the LGPL license from the original plugin-cathare project.

## Links

- [CATHARE Website](http://www-cathare.cea.fr/)
- [Funz Framework](https://github.com/Funz/fz)
- [Original Plugin](https://github.com/Funz/plugin-cathare)