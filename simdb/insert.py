import os
import time as ttime
from uuid import uuid4
import simdb
from ase import io as aseio
from .utils import _ensure_connection
from .odm_templates import *
from filestore import commands as fsc

__author__ = 'christopher'



@_ensure_connection
def insert_simulation_parameters(name, temperature, iterations,
                                 target_acceptance, time=None):
    if time is None:
        time = ttime.time()
    sp = SimulationParameters(name=name, temperature=temperature,
                              iterations=iterations,
                              target_acceptance=target_acceptance,
                              time=time)
    # save the document
    sp.save(validate=True, write_concern={"w": 1})
    return sp


@_ensure_connection
def insert_atom_document(name, ase_object, time=None):
    if time is None:
        time = ttime.time()
    # at some level, you dont actually care where this thing is on disk
    file_uid = str(uuid4())

    is_trajectory = False
    if isinstance(ase_object, list):
        is_trajectory = True

    # create the filename
    file_name = os.path.join(simdb.ATOM_PATH, file_uid + '.traj')
    # save the object
    aseio.write(file_name, ase_object)

    # do the filestore magic
    resource = fsc.insert_resource('ase', file_name)
    fsc.insert_datum(resource, file_uid,
                     datum_kwargs={'is_trajectory': is_trajectory})

    # create an instance of a mongo document (metadata)
    a = AtomicConfig(name=name, file_uid=file_uid, time=time)
    # save the document
    a.save()
    return a
