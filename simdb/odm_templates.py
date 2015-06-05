"""
ODM templates for use with metadatstore
"""
from mongoengine import Document, DynamicDocument, DynamicEmbeddedDocument
from mongoengine import (StringField, DictField, IntField, FloatField,
                         ListField, ReferenceField, EmbeddedDocumentField,
                         DENY, MapField)
from mongoengine import connect
from getpass import getuser
import time as ttime
import filestore
from filestore import commands as fsc
from uuid import uuid4
import os
import ase

ALIAS = 'simdb'

ATOM_PATH = os.path.join(os.path.expanduser('~'), 'data', 'ase-atoms')

connection_config = {'host': 'localhost',
                     'database': 'simdb',
                     'port': 27017,
                     'timezone': 'US/Eastern'}

# create the ase handler
def ASE_file_handler(*args, **kwargs):
    # this is almost certainly incorrect
    # see filestore.handlers.py for more info
    return ase.io.read(*args, **kwargs)

# create the pickle handler


def find_atom_document(**kwargs):
    atoms = Atom.objects(__raw__=kwargs).order_by('-_id')
    for atom in atoms:
        atom.file_payload = fsc.retrieve(atom.file_uid)
    return atoms


def insert_atom_document(name, ase_object, time=None):
    if time is None:
        time = ttime.time()
    # at some level, you dont actually care where this thing is on disk
    file_uid = uuid4()
    # create the filename
    file_name = os.path.join(ATOM_PATH, file_uid)
    # save the object
    ase_object.save(file_name)
    # do the filestore magic
    resource = fsc.insert_resource('ase')
    fsc.insert_datum(resource, file_uid, file_path=file_name)
    # create an instance of a mongo document
    a = Atom(name=name, file_path=file_uid, time=time)
    # save the document
    a.save()
    return a


class Atom(DynamicDocument):
    name = StringField(required=False)
    file_uid = StringField(required=True, unique=True)
    time = FloatField(required=True)
    meta = {'indexes': ['_id', 'name']}


class SimulationParameters(DynamicDocument):
    temperature = FloatField(required=True)
    iterations = IntField(required=True)
    target_acceptance = FloatField(required=True)
    time = FloatField(required=True)
    meta = {'indexes': ['temperature']}


class Simulation(DynamicDocument):

    # references to input data
    params = ReferenceField(SimulationParameters, reverse_delete_rule=DENY,
                            required=True,
                            db_field='params_id')
    atoms = ReferenceField(Atom, reverse_delete_rule=DENY, required=True,
                           db_field='atoms_id')

    # actual simulation stuff
    final_energy = FloatField(required=True)
    name = StringField(required=True)
    start_time = FloatField(required=True)
    end_time = FloatField(required=True)

    # trajectory file
    traj_file_uid = StringField(required=True)
