__author__ = 'christopher'
import ase
from simdb.insert import *
from simdb.search import *
from pyiid.utils import build_sphere_np
from copy import deepcopy as dc

# Read in the parent atoms
parent_atoms = ase.io.read(
    '/mnt/bulk-data/Dropbox/BNL_Project/Simulations/Models.d/1-C60.d/C60.xyz')
target_config = insert_atom_document('C60 DFT', parent_atoms)

# Now load the G(r) data, this is not needed if it is already in the DB
pdf = insert_pdf_data_document('C60 DFT Target', atomic_config=target_config)

# Cut the rmin and rmax data
exp_dict = pdf.pdf_params
exp_dict['qmin'] = .1
exp_dict['rmin'] = 1.2
exp_dict['rmax'] = 8.

# Now create the kwargs for the two calculators: PDF and Spring
calc_kwargs1 = {'conv': 300, 'potential': 'rw', 'exp_dict': exp_dict}
calc1 = insert_calc('C60 Rw', 'PDF', calc_kwargs1, calc_exp=pdf)

calc_kwargs2 = {'k': 500, 'rt': exp_dict['rmin']}
calc2 = insert_calc('C60 spring', 'Spring', calc_kwargs2)

# Create the combined Potential Energy Surface (PES)
# calc_list = [calc1, calc2]
# pes = insert_pes('C60 PDF Spring', calc_list)
pes, = find_pes_document(name='C60 PDF Spring')

# Create the simulation parameters
# params = insert_simulation_parameters('T=1, iter=100, accept=.65', 1, 100, .65,
#                                       continue_sim=True)
params, = find_simulation_parameter_document(name='T=1, iter=100, accept=.65')

rattles = [.05, .07, .08, .1]
for rattle in rattles:
    # rattle the starting position
    starting_atoms = dc(parent_atoms)
    starting_atoms.rattle(rattle)

    # Add the atoms to the DB
    start_config = insert_atom_document('C60 ' + str(rattle), starting_atoms)
    # Finally create the simulation
    sim = insert_simulation('C60 rattle->DFT ' + str(rattle), params, start_config, pes)
    print 'simulation added, number ', sim.id
