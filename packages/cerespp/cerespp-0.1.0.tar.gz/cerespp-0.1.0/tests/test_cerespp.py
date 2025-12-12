import cerespp
import os
import pytest
import pandas as pd

def test_get_activities(example_fits_files, tmp_path):
    if not example_fits_files:
        pytest.skip("No example FITS files found")
    
    # Use tmp_path for output
    out_dir = tmp_path / "output"
    
    files = [str(f) for f in example_fits_files]
    
    # Run the main function
    df, header = cerespp.get_activities(files, str(out_dir))
    
    # Assertions
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == len(files)
    assert "S" in df.columns
    assert "Halpha" in df.columns
    
    # Check if output file was created
    dat_files = list(out_dir.glob("*.dat"))
    assert len(dat_files) > 0

def test_get_activities_no_save(example_fits_files):
    if not example_fits_files:
        pytest.skip("No example FITS files found")
        
    files = [str(f) for f in example_fits_files]
    
    # Run without output directory (in-memory only)
    df, header = cerespp.get_activities(files, out=None, save_activities=False)
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == len(files)
