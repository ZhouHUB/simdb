__author__ = 'christopher'
"""
This use case examines how to submit to the db using experimental data starting
with a previously refined 2nm Au structure based on PDF+FF
Note: This is the first run on the DB for this work, so everything needs to be
entered, once the DB is more fully populated then many of the insert_*
statements can be replaced with find_* statements, with associated changes made
to the internal parameters, followed by a obj.save() call.
"""
import ase
from simdb.insert import *
from simdb.search import *
from pyiid.utils import build_sphere_np


# Read in the starting atoms
starting_atoms = build_sphere_np('/mnt/work-data/dev/IID_data/examples/SnOx/1000062.cif', 23./2)

# Make the atoms Unit Mass
starting_atoms.set_masses(np.ones(len(starting_atoms)))
# Add the atoms to the DB
start_config = insert_atom_document('2.3nm SnO2 Crystal unit mass', starting_atoms)

# Now load the G(r) data, this is not needed if it is already in the DB
gr_file_loc = '/mnt/work-data/dev/IID_data/examples/SnOx/SnO2_300K-sum_00608_637_sqmsklargemsk.gr'
pdf = insert_pdf_data_document('2.3nm SnO3 PDF data', input_filename=gr_file_loc)

# Cut the rmin and rmax data
exp_dict = pdf.pdf_params
exp_dict['rmin'] = 1.5
exp_dict['rmax'] = 30.

# Now create the kwargs for the two calculators: PDF and Spring
calc_kwargs1 = {'conv': 300, 'potential': 'rw', 'exp_dict': exp_dict}
calc1 = insert_calc('2.3nm SnO2 PDF Rw calc', 'PDF', calc_kwargs1, calc_exp=pdf)

calc_kwargs2 = {'k': 100, 'rt': exp_dict['rmin']}
calc2 = insert_calc('test spring', 'Spring', calc_kwargs2)

# Create the combined Potential Energy Surface (PES)
calc_list = [calc1, calc2]
pes = insert_pes('PDF Spring', calc_list)

# Create the simulation parameters
params = insert_simulation_parameters('test param', 1., 100, .65)

# Finally create the simulation
sim = insert_simulation('2.3nm SnO2 unit mass PDF+Spring', params, start_config, pes)
print 'simulation added, number ', sim.id
