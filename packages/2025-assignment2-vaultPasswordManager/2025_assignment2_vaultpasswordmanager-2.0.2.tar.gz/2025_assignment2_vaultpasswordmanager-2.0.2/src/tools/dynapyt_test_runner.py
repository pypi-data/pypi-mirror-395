import pytest
import sys
import os

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

if __name__ == "__main__":
    # Run pytest on the unittest directory
    print("Starting DynaPyt Test Runner...")
    # -s: Disable output capturing so DynaPyt logs are visible
    ret = pytest.main(["src/unittest", "-s"])
    sys.exit(ret)
