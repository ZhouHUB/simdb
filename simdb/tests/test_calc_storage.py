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
    calc_kwargs = {'k': 100, 'rt': 2.4}
    a = insert_calc('test spring', 'Spring', calc_kwargs)
    ret, = find_calc_document(_id=a.id)

    local_calc = Spring(**calc_kwargs)
    print local_calc, ret.payload
    # make sure the retrieved document got something from filestore
    assert(hasattr(ret, 'payload'))
    # make sure the payload is equivalent to the original atoms
    atoms = ase.Atoms('Au2', [[0, 0, 0], [0, 0, 3]])
    atoms.set_calculator(local_calc)
    l_force = atoms.get_forces()
    l_energy = atoms.get_potential_energy()

    atoms.set_calculator(ret.payload)
    re_force = atoms.get_forces()
    re_energy = atoms.get_potential_energy()
    # assert(local_calc == ret.payload)
    assert(np.all(l_force == re_force))
    assert(l_energy == re_energy)
    # make sure that the bits that came back from filestore are a different
    # object
    assert_not_equal(id(local_calc), id(ret.payload))
