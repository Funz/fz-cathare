#!/usr/bin/env python3
"""
Test script to validate CATHARE output parsing.

This script verifies that the parsed output matches expected values from the
FORT07 file format.
"""

import sys
import os

try:
    import fz
except ImportError:
    print("Error: fz framework not installed. Install with: pip install fz")
    sys.exit(1)


def test_output_parsing():
    """Test CATHARE output parsing against known values."""
    
    test_output_dir = os.path.join(
        os.path.dirname(__file__),
        "CNV22",
        "output"
    )
    
    if not os.path.exists(test_output_dir):
        print(f"Error: Test directory not found at {test_output_dir}")
        return False
    
    print("Testing CATHARE output parsing...")
    print(f"Test directory: {test_output_dir}")
    print()
    
    # Parse the output
    try:
        results = fz.fzo(test_output_dir, model="Cathare")
    except Exception as e:
        print(f"✗ Failed to parse output: {e}")
        return False
    
    # Extract the output dictionary
    if '*' not in results.columns or len(results) == 0:
        print("✗ No output data found")
        return False
    
    output_dict = results['*'].iloc[0]
    
    if not isinstance(output_dict, dict):
        print(f"✗ Unexpected output format: {type(output_dict)}")
        return False
    
    # Test 1: Check that expected variables exist
    print("Test 1: Checking for expected variables...")
    expected_vars = ['ML', 'TIME_ML', 'MV', 'TIME_MV', 'MTOT', 'TIME_MTOT',
                     'P0', 'TIME_P0', 'P8', 'TIME_P8', 'QL', 'TIME_QL', 
                     'QV', 'TIME_QV', 'DUM0', 'TIME_DUM0', 'DUM8', 'TIME_DUM8']
    
    missing_vars = [v for v in expected_vars if v not in output_dict]
    if missing_vars:
        print(f"✗ Missing variables: {missing_vars}")
        return False
    print(f"✓ All {len(expected_vars)} expected variables found")
    
    # Test 2: Check data lengths match
    print("\nTest 2: Checking data lengths...")
    time_ml_len = len(output_dict['TIME_ML'])
    ml_len = len(output_dict['ML'])
    
    if time_ml_len != ml_len:
        print(f"✗ Length mismatch: TIME_ML has {time_ml_len} points, ML has {ml_len} points")
        return False
    print(f"✓ TIME_ML and ML both have {ml_len} points")
    
    # Test 3: Validate specific known values from FORT07
    print("\nTest 3: Validating specific values...")
    
    # TIME values (from line 6-7 of FORT07)
    # TIME[0] = 0.00000000E+000 = 0.0
    # TIME[1] = 0.81098631E+000 = 0.810986
    # TIME[2] = 0.13109863E+001 = 1.310986
    expected_times = [0.0, 0.810986, 1.310986, 1.810986, 2.310986]
    actual_times = output_dict['TIME_ML'][:5]
    
    for i, (expected, actual) in enumerate(zip(expected_times, actual_times)):
        if abs(expected - actual) > 1e-5:
            print(f"✗ TIME_ML[{i}] mismatch: expected {expected}, got {actual}")
            return False
    print(f"✓ TIME_ML values correct (checked first 5)")
    
    # ML (LIQMASS) values (from line 172-173 of FORT07)
    # ML[0] = 0.29076885E+002 = 29.076885
    # ML[1] = 0.28502382E+002 = 28.502382
    expected_ml = [29.076885, 28.502382, 28.23147, 27.992447, 27.772408]
    actual_ml = output_dict['ML'][:5]
    
    for i, (expected, actual) in enumerate(zip(expected_ml, actual_ml)):
        if abs(expected - actual) > 1e-5:
            print(f"✗ ML[{i}] mismatch: expected {expected}, got {actual}")
            return False
    print(f"✓ ML values correct (checked first 5)")
    
    # Test 4: Check that TIME_* variables are x-axis for their corresponding data
    print("\nTest 4: Checking TIME_* and Z_* consistency...")
    for var_name in ['ML', 'MV', 'MTOT', 'P0', 'P8', 'QL', 'QV', 'DUM0', 'DUM8']:
        if var_name in output_dict:
            # Check if TIME_* or Z_* exists
            time_var = f'TIME_{var_name}'
            z_var = f'Z_{var_name}'
            
            if time_var in output_dict:
                if len(output_dict[time_var]) != len(output_dict[var_name]):
                    print(f"✗ Length mismatch: {time_var} and {var_name}")
                    return False
            elif z_var in output_dict:
                if len(output_dict[z_var]) != len(output_dict[var_name]):
                    print(f"✗ Length mismatch: {z_var} and {var_name}")
                    return False
            else:
                print(f"✗ Missing x-axis for {var_name}")
                return False
    
    print("✓ All variables have matching x-axis data")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_output_parsing()
    sys.exit(0 if success else 1)
