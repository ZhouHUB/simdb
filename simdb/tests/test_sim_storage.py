__author__ = 'christopher'
import simdb
from uuid import uuid4
import simdb
from simdb.odm_templates import AtomicConfig, SimulationParameters
from simdb.insert import *
from simdb.search import *
import time as ttime
import tempfile
import ase
from simdb.utils.testing import simdb_setup, simdb_teardown
from nose.tools import assert_equal, assert_not_equal

def setup():
    simdb_setup()
    simdb.PDF_PATH = tempfile.gettempdir()
    simdb.ATOM_PATH = tempfile.gettempdir()


def teardown():
    # gets run last
    simdb_teardown()


def test_insert_and_retrieve_fabricated_data():
    from pyiid.calc.spring_calc import Spring
    from pyiid.calc.multi_calc import MultiCalc
    atoms = ase.Atoms('Au2', [[0, 0, 0], [0, 0, 3]])
    db_atoms = insert_atom_document('au2', atoms)


    calc_kwargs1 = {'k': 100, 'rt': 2.4}
    calc_kwargs2 = {'k': 500, 'rt': 2.0}
    a = insert_calc('test spring', 'Spring', calc_kwargs1)
    b = insert_calc('test spring', 'Spring', calc_kwargs2)

    calc_list = [a, b]

    c = insert_pes('Double Spring', calc_list)

    params = insert_simulation_parameters('test param', 1., 100, .65)

    sim = insert_simulation('test sim', params, db_atoms, c)

    ret, = find_simulation_document(_id=sim.id)

    sim_params, = find_simulation_parameter_document(_id=ret.params.id)
    assert 100 == sim_params.iterations
    assert .65 == sim_params.target_acceptance
    assert 1. == sim_params.temperature
