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
        r = s.get_r()

        # get the atomic configuration from the DB
        atomic_doc = find_atomic_config_document(_id=atomic_config.id)
        atoms = atomic_doc.file_payload

        # Generate the PDF from the atomic configuration
        gobs = s.get_pdf(atoms)
        generated = True

        # Save the gobs
        np.save(file_name, gobs)
        res = fsc.insert_resource('genpdf', file_name)
        fsc.insert_datum(res, file_uid)
    else:
        # Then the pdf is experimental, thus we should let filestore know it
        # exists, an load the PDF generating parameters into the Metadata
        res = fsc.insert_resource('pdfgetx3', input_filename)
        fsc.insert_datum(res, file_uid)
        r, gobs, params = load_gr_file(input_filename)

    # create an instance of a mongo document (metadata)
    if generated is True:
        a = PDFData(name=name, file_uid=file_uid, ase_config_id=atomic_config,
                    pdf_params=exp_dict, time=time)
    else:
        a = PDFData(name=name, file_uid=file_uid,
                    # will support when we mirge this with metadata store
                    # experiment_uid=exp_uid,
                    pdf_params=params, time=time)
    # save the document
    a.save()
    return a