""" Tests for calculations

"""
import os

from aiida.engine import run
from aiida.plugins import CalculationFactory, DataFactory

from . import TEST_DIR


def run_pdb2gmx(gromacs_code):
    """ Run an instance of pdb2gmx and return the results."""

    # Prepare input parameters
    Pdb2gmxParameters = DataFactory("gromacs.pdb2gmx")
    parameters = Pdb2gmxParameters(
        {
            "ff": "oplsaa",
            "water": "spce",
            "o": "pdb2gmx_1AKI_forcefield.gro",
            "p": "pdb2gmx_1AKI_topology.top",
            "i": "pdb2gmx_1AKI_restraints.itp",
        }
    )

    SinglefileData = DataFactory("core.singlefile")
    pdbfile = SinglefileData(
        file=os.path.join(TEST_DIR, "input_files", "pdb2gmx_1AKI_clean.pdb")
    )

    # set up calculation
    inputs = {
        "code": gromacs_code,
        "parameters": parameters,
        "pdbfile": pdbfile,
        "metadata": {
            "description": "pdb2gmx test",
        },
    }

    result = run(CalculationFactory("gromacs.pdb2gmx"), **inputs)

    return result


def test_process(gromacs_code):
    """Test running a pdb2gmx calculation.
    Note: this does not test that the expected outputs are created of output parsing"""

    result = run_pdb2gmx(gromacs_code)

    assert "stdout" in result
    assert "grofile" in result
    assert "itpfile" in result
    assert "topfile" in result


def test_file_name_match(gromacs_code):
    """Test that the file names returned match what was specified on inputs."""
    
    result = run_pdb2gmx(gromacs_code)

    assert result["stdout"].base.repository.list_object_names()[0] == "pdb2gmx.out"
    assert result["grofile"].base.repository.list_object_names()[0] == "pdb2gmx_1AKI_forcefield.gro"
    assert result["topfile"].base.repository.list_object_names()[0] == "pdb2gmx_1AKI_topology.top"
    assert result["itpfile"].base.repository.list_object_names()[0] == "pdb2gmx_1AKI_restraints.itp"

