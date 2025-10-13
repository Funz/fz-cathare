#!/usr/bin/env python3
"""
Example script demonstrating the fz-cathare plugin.

This script shows how to parse CATHARE output files using the fz framework.
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
        print(f"\nFound {len(results.columns)} output variables:")
        
        # Display available variables
        for col in sorted(results.columns):
            if col != 'path':
                value = results[col].iloc[0] if len(results) > 0 else None
                if isinstance(value, list):
                    print(f"  - {col}: {len(value)} data points")
                else:
                    print(f"  - {col}: {value}")
        
        # Show some sample data
        print("\n" + "=" * 60)
        print("Sample Data")
        print("=" * 60)
        
        # Try to show TIME_ML and ML as an example
        for var in ['TIME_ML', 'ML']:
            if var in results.columns:
                data = results[var].iloc[0] if len(results) > 0 else None
                if isinstance(data, list) and len(data) > 0:
                    print(f"\n{var} (first 5 values):")
                    for i, val in enumerate(data[:5]):
                        print(f"  [{i}] {val}")
        
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
