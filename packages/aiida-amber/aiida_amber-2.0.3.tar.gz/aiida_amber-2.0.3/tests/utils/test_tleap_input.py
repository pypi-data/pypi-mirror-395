"""Test for tleap file class"""

import pytest
import os
from aiida_amber.data.tleap_input import TleapInputData, parse_tleap_input_file
from .. import TEST_DIR


@pytest.fixture
def tleapdatafile():
    yield TleapInputData(os.path.join(TEST_DIR, "input_files", "tleap", "tleap_syntax.in"))


def test_parse_tleap_input_file(tleapdatafile):
    """Check tleap input file is parsed correctly"""
    expected_inputs = ['dir1/LigandA.mol2', 
                       'dir1/LigandB.mol2', 
                       'dir1/LigandC.mol2', 
                       'dir1/LigandA.frcmod', 
                       'dir1/LigandB.frcmod', 
                       'dir1/LigandC.frcmod', 
                       'dir2/Protein.pdb']
    expected_outputs = ['complex.prmtop', 'complex.inpcrd']
    assert tleapdatafile.inpfile_list == expected_inputs
    assert tleapdatafile.outfile_list == expected_outputs

# def test_tleap_data_creation():
#     inputs = {}
#     # Prepare input parameters in AiiDA formats.
#     inputs["tleapfile"] = TleapInputData(file=os.path.join(TEST_DIR, "input_files", "tleap.in"))