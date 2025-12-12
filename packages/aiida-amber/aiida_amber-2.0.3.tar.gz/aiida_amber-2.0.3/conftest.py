"""pytest fixtures for simplified testing."""
import pytest

pytest_plugins = ["aiida.manage.tests.pytest_fixtures"]


@pytest.fixture(scope="function", autouse=True)
def clear_database_auto(clear_database):  # pylint: disable=unused-argument
    """Automatically clear database in between tests."""


@pytest.fixture(scope="function")
def amber_code(aiida_local_code_factory):
    """Get sander code."""
    return aiida_local_code_factory(executable="sander", entry_point="amber")


@pytest.fixture(scope="function")
def tleap_code(aiida_local_code_factory):
    """Get tleap code."""
    return aiida_local_code_factory(executable="tleap", entry_point="amber")


@pytest.fixture(scope="function")
def antechamber_code(aiida_local_code_factory):
    """Get antechamber code."""
    return aiida_local_code_factory(executable="antechamber", entry_point="amber")


@pytest.fixture(scope="function")
def pdb4amber_code(aiida_local_code_factory):
    """Get pdb4amber code."""
    return aiida_local_code_factory(executable="pdb4amber", entry_point="amber")


@pytest.fixture(scope="function")
def parmed_code(aiida_local_code_factory):
    """Get parmed code."""
    return aiida_local_code_factory(executable="parmed", entry_point="amber")


@pytest.fixture(scope="function")
def bash_code(aiida_local_code_factory):
    """Get bash code."""
    return aiida_local_code_factory(executable="bash", entry_point="amber")
