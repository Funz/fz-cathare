#!/usr/bin/env python3
"""
Example demonstrating a complete parametric study workflow with fz-cathare.

This script shows how to:
1. Detect variables in input files
2. Compile input files with different parameter values
3. Parse CATHARE output files
"""

import sys
import os

# Add parent directory to path if running from repo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import fz
except ImportError:
    print("Error: fz framework not installed. Install with: pip install fz")
    sys.exit(1)


def demo_variable_detection():
    """Demonstrate variable detection in input files."""
    print("=" * 70)
    print("STEP 1: Variable Detection (fzi)")
    print("=" * 70)
    
    input_file = "tests/example_parametric.txt"
    
    if not os.path.exists(input_file):
        print(f"Error: Example file not found: {input_file}")
        return None
    
    print(f"\nAnalyzing input file: {input_file}")
    
    variables = fz.fzi(input_file, model="Cathare")
    
    print(f"\nFound {len(variables)} variables:")
    for var in sorted(variables.keys()):
        print(f"  - ${var}")
    
    return variables


def demo_input_compilation():
    """Demonstrate input file compilation with parameter substitution."""
    print("\n" + "=" * 70)
    print("STEP 2: Input Compilation (fzc)")
    print("=" * 70)
    
    input_file = "tests/example_parametric.txt"
    
    # Define parameter values for a parametric study
    # We'll create a grid of 2x2 = 4 cases
    param_values = {
        "temperature": [300, 350],    # 2 temperature values
        "pressure": [101325, 200000], # 2 pressure values
        "flow_rate": 1.5,             # Fixed value
        "area": 0.01                  # Fixed value
    }
    
    print(f"\nParameter grid:")
    print(f"  temperature: {param_values['temperature']}")
    print(f"  pressure: {param_values['pressure']}")
    print(f"  flow_rate: {param_values['flow_rate']} (fixed)")
    print(f"  area: {param_values['area']} (fixed)")
    
    output_dir = "/tmp/cathare_param_study"
    
    print(f"\nCompiling input files to: {output_dir}")
    
    fz.fzc(input_file, param_values, model="Cathare", output_dir=output_dir)
    
    # List the generated directories
    if os.path.exists(output_dir):
        subdirs = [d for d in os.listdir(output_dir) 
                   if os.path.isdir(os.path.join(output_dir, d))]
        print(f"\n✓ Created {len(subdirs)} case directories:")
        for subdir in sorted(subdirs):
            print(f"  - {subdir}")
    
    return output_dir


def demo_output_parsing():
    """Demonstrate output parsing from CATHARE results."""
    print("\n" + "=" * 70)
    print("STEP 3: Output Parsing (fzo)")
    print("=" * 70)
    
    # Use the existing test output
    output_dir = "tests/CNV22/output"
    
    print(f"\nParsing CATHARE output from: {output_dir}")
    
    results = fz.fzo(output_dir, model="Cathare")
    
    if '*' in results.columns and len(results) > 0:
        output_dict = results['*'].iloc[0]
        
        print(f"\n✓ Successfully parsed {len(output_dict)} output variables:")
        
        # Show some key variables
        key_vars = ['ML', 'MV', 'P0', 'P8']
        for var in key_vars:
            if var in output_dict:
                data = output_dict[var]
                if isinstance(data, list) and len(data) > 0:
                    print(f"\n  {var}:")
                    print(f"    - Data points: {len(data)}")
                    print(f"    - First value: {data[0]:.6f}")
                    print(f"    - Last value: {data[-1]:.6f}")
                    
                    # Show corresponding TIME/Z axis
                    time_var = f"TIME_{var}"
                    z_var = f"Z_{var}"
                    if time_var in output_dict:
                        time_data = output_dict[time_var]
                        print(f"    - Time range: {time_data[0]:.2f} to {time_data[-1]:.2f} seconds")
                    elif z_var in output_dict:
                        z_data = output_dict[z_var]
                        print(f"    - Z range: {z_data[0]:.2f} to {z_data[-1]:.2f} meters")
    
    return results


def demo_full_workflow():
    """Demonstrate the complete workflow."""
    print("\n" + "=" * 70)
    print("CATHARE Parametric Study Workflow Demonstration")
    print("=" * 70)
    print()
    
    # Step 1: Variable detection
    variables = demo_variable_detection()
    if variables is None:
        return
    
    # Step 2: Input compilation
    demo_input_compilation()
    
    # Step 3: Output parsing
    demo_output_parsing()
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
In a real parametric study with CATHARE, the workflow would be:

1. Create input template with variables (using $ prefix)
2. Define parameter ranges
3. Use fz.fzr() to:
   - Compile inputs for all parameter combinations
   - Run CATHARE calculations (in parallel if configured)
   - Parse all outputs
   - Return results as a pandas DataFrame

Example code:
    
    results = fz.fzr(
        input_path="cathare_input.dat",
        input_variables={
            "temperature": [300, 350, 400],
            "pressure": [1e5, 2e5, 3e5]
        },
        model="Cathare",
        calculators="sh://cathare",
        results_dir="results"
    )
    
This would run 3x3 = 9 CATHARE simulations and collect all results.
""")
    
    print("=" * 70)
    print("Demo complete!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        demo_full_workflow()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
