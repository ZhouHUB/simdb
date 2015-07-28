__author__ = 'christopher'
import ase
from simdb.insert import *
from simdb.search import *
from pyiid.utils import build_sphere_np
from copy import deepcopy as dc

target_config, = find_atomic_config_document(name='C60 DFT')
parent_atoms = target_config.file_payload[-1]

# find the combined Potential Energy Surface (PES)

pes, = find_pes_document(name='C60 PDF Spring')

# find the simulation parameters

params, = find_simulation_parameter_document(name='T=1, iter=100, accept=.65')

rattles = [.05, .07, .08, .1]
for rattle in rattles:
    # find starting_config
    try:
        start_config, = find_atomic_config_document(name='C60' + str(rattle))
    except ValueError:
        starting_atoms = dc(parent_atoms)
        starting_atoms.rattle(rattle, 42)

        # Add the atoms to the DB
        start_config = insert_atom_document('C60 ' + str(rattle), starting_atoms)

    # Finally create the simulation
    sim = insert_simulation('C60 rattle->DFT ' + str(rattle), params, start_config, pes)
    print 'simulation added, number ', sim.id
