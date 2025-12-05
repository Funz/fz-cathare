#!/usr/bin/env python3
"""
Example script demonstrating the fz-cathare plugin.

This script shows how to parse CATHARE output files using the fz framework.
"""

import sys
import os

try:
    import fz
except ImportError:
    print("Error: fz framework not installed. Install with: pip install fz")
    sys.exit(1)


def main():
    """Parse sample CATHARE output and display results."""
    
    # Path to test output directory
    test_output_dir = os.path.join(
        os.path.dirname(__file__),
        "tests",
        "CNV22",
        "output"
    )
    
    if not os.path.exists(test_output_dir):
        print(f"Error: Test directory not found at {test_output_dir}")
        sys.exit(1)
    
    print("=" * 60)
    print("CATHARE Output Parsing Example")
    print("=" * 60)
    print(f"\nParsing output from: {test_output_dir}")
    print()
    
    # Parse the output using the Cathare model
    try:
        results = fz.fzo(test_output_dir, model="Cathare")
        
        if results is None or (hasattr(results, 'empty') and results.empty):
            print("No results parsed from output files.")
            return
        
        print(f"Successfully parsed CATHARE output!")
        
        # The Cathare model returns all outputs in a dictionary under the '*' column
        # This is because CATHARE output variables are dynamic (not known in advance)
        if '*' in results.columns and len(results) > 0:
            output_dict = results['*'].iloc[0]
            
            if isinstance(output_dict, dict):
                print(f"\nFound {len(output_dict)} output variables:")
                
                # Display available variables
                for var_name in sorted(output_dict.keys()):
                    value = output_dict[var_name]
                    if isinstance(value, list):
                        print(f"  - {var_name}: {len(value)} data points")
                    else:
                        print(f"  - {var_name}: {value}")
                
                # Show some sample data
                print("\n" + "=" * 60)
                print("Sample Data")
                print("=" * 60)
                
                # Try to show TIME_ML and ML as an example
                for var in ['TIME_ML', 'ML', 'TIME_MV', 'MV']:
                    if var in output_dict:
                        data = output_dict[var]
                        if isinstance(data, list) and len(data) > 0:
                            print(f"\n{var} (first 5 values):")
                            for i, val in enumerate(data[:5]):
                                print(f"  [{i}] {val:.6f}")
            else:
                print(f"\nUnexpected output format: {type(output_dict)}")
        else:
            print("\nNo output data found in '*' column")
        
        print("\n" + "=" * 60)
        print("Example complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error parsing output: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
