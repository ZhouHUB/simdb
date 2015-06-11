__author__ = 'christopher'
import ase.io as aseio

from simdb.insert import insert_atom_document, insert_simulation_parameters, \
    insert_pes, insert_simulation, insert_calc


# Create Atoms
atoms = aseio.read('filename')
atoms = insert_atom_document('Au55 relaxed', atoms)

# Create calcs
calc_l = []
calcs = [
    {'name': 'PDF', 'kwargs': {'conv': 300, 'potential': 'rw'}},
    {'name': 'Spring', 'kwargs': {'k': 100, 'rt': 'rmin'}},
]
for calc in calcs:
    calc_l.append(insert_calc(name=calc['name'], kwargs=calc['kwargs']))

# Create PES
pes = insert_pes(name='RW+Spring', calc_list=calc_l)

# Create Simulation Parameters
params = insert_simulation_parameters('standard 100', 1, 100, .65)

# Log everything
sim = insert_simulation(name='Au55 relaxed to disordered', params=params,
                        atoms=atoms, pes=pes)

# Start Simulation or restart simulation or continue simulation
output = run_simulation(sim)

# Run analysis
run_analysis(output)
