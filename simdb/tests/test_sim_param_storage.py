import simdb
from uuid import uuid4
import simdb
from simdb.odm_templates import AtomicConfig, SimulationParameters
from simdb.insert import insert_atom_document, insert_simulation_parameters
from simdb.search import find_simulation_parameter_document
import time as ttime
import tempfile
import ase
from simdb.utils.testing import simdb_setup, simdb_teardown
from nose.tools import assert_equal, assert_not_equal


def setup():
    simdb_setup()
    simdb.ATOM_PATH = tempfile.gettempdir()


def teardown():
    # gets run last
    simdb_teardown()


def test_insert_and_retrieve():

    a = insert_simulation_parameters('test param', 1., 100, .65)
    ret, = find_simulation_parameter_document(_id=a.id)

    assert(1. == ret.temperature)
    assert(100 == ret.iterations)
    assert(.65 == ret.target_acceptance)
    assert(True == ret.continue_sim)
