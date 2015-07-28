import os
import time as ttime
from uuid import uuid4
import simdb
from ase import io as aseio
from .utils import _ensure_connection
from .odm_templates import *
from filestore import commands as fsc
from pyiid.utils import load_gr_file
from pyiid.wrappers.elasticscatter import ElasticScatter as Scatter
import numpy as np
from .search import find_atomic_config_document

__author__ = 'christopher'



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


@_ensure_connection
def insert_pdf_data_document(name, input_filename=None,
                             atomic_config=None, exp_dict=None, time=None):
    if time is None:
        time = ttime.time()
    # at some level, you dont actually care where this thing is on disk
    file_uid = str(uuid4())
    # create the filename
    file_name = os.path.join(simdb.PDF_PATH, file_uid + '.gr')

    generated = False
    if atomic_config is not None:
        # Then we should generate the PDF
        s = Scatter(exp_dict)

        # Just in case we use the exp_dict = None default params
        params = s.exp

        # get the atomic configuration from the DB
        atomic_doc, = find_atomic_config_document(_id=atomic_config.id)
        atoms = atomic_doc.file_payload[-1]

        # Generate the PDF from the atomic configuration
        gobs = s.get_pdf(atoms)
        generated = True

        # Save the gobs
        # TODO: replace with context
        f = open(file_name, 'w')
        np.save(f, gobs)
        f.close()
        res = fsc.insert_resource('genpdf', file_name)
        fsc.insert_datum(res, file_uid)
    else:
        # Then the pdf is experimental, thus we should let filestore know it
        # exists, and load the PDF generating parameters into the Metadata
        res = fsc.insert_resource('pdfgetx3', input_filename)
        fsc.insert_datum(res, file_uid)
        params = load_gr_file(input_filename)[-1]

    # create an instance of a mongo document (metadata)
    if generated is True:
        a = PDFData(name=name, file_uid=file_uid, ase_config_id=atomic_config,
                    pdf_params=params, time=time)
    else:
        a = PDFData(name=name, file_uid=file_uid,
                    # will support when we merge this with metadata store
                    # experiment_uid=exp_uid,
                    pdf_params=params, time=time)
    # save the document
    a.save()
    return a


@_ensure_connection
def insert_calc(name, calculator, calc_kwargs, calc_exp=None, time=None):
    if time is None:
        time = ttime.time()
    if calc_exp is not None:
        calc = Calc(name=name, calculator=calculator, calc_kwargs=calc_kwargs,
                    calc_exp=calc_exp, time=time)
    else:
        calc = Calc(name=name, calculator=calculator, calc_kwargs=calc_kwargs,
                    time=time)
    # save the document
    calc.save(validate=True, write_concern={"w": 1})
    return calc


@_ensure_connection
def insert_pes(name, calc_list, time=None):
    if time is None:
        time = ttime.time()
    pes = PES(name=name, calc_list=calc_list,
              time=time)
    # save the document
    pes.save(validate=True, write_concern={"w": 1})
    return pes


@_ensure_connection
def insert_simulation_parameters(name, temperature, iterations,
                                 target_acceptance=.65, continue_sim=True,
                                 time=None):
    if time is None:
        time = ttime.time()
    sp = SimulationParameters(name=name, temperature=temperature,
                              iterations=iterations,
                              target_acceptance=target_acceptance,
                              continue_sim=continue_sim,
                              time=time)
    # save the document
    sp.save(validate=True, write_concern={"w": 1})
    return sp


@_ensure_connection
def insert_simulation(name, params, atoms, pes, skip=False, time=None):
    if time is None:
        time = ttime.time()
    sp = Simulation(name=name, params=params, atoms=atoms, pes=pes, skip=skip)
    # save the document
    sp.save(validate=True, write_concern={"w": 1})
    return sp
