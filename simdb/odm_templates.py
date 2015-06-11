"""
ODM templates for use with metadatstore
"""
from functools import wraps
import os

from mongoengine import DynamicDocument
from mongoengine import (StringField, DictField, IntField, FloatField,
                         ReferenceField, BooleanField, ListField, DENY)
from mongoengine import connect
import mongoengine
import simdb

ATOM_PATH = os.path.join('/mnt/bulk_data/', 'data', 'ase-atoms')


def _ensure_connection(func):
    @wraps(func)
    def inner(*args, **kwargs):
        database = simdb.connection_config['database']
        host = simdb.connection_config['host']
        port = int(simdb.connection_config['port'])
        connect(db=database, host=host, port=port, alias=simdb.DATABASE_ALIAS)
        return func(*args, **kwargs)

    return inner


def db_disconnect():
    """Helper function to deal with stateful connections to mongoengine"""
    mongoengine.connection.disconnect(simdb.DATABASE_ALIAS)
    for collection in [AtomicConfig, SimulationParameters, Simulation]:
        collection._collection = None


def db_connect(database, host, port):
    print('database = %s' % database)
    print('host = %s' % host)
    print('port = %s' % port)
    """Helper function to deal with stateful connections to mongoengine"""
    return connect(db=database, host=host, port=port,
                   alias=simdb.DATABASE_ALIAS)


class AtomicConfig(DynamicDocument):
    name = StringField(required=False)
    file_uid = StringField(required=True, unique=True)
    time = FloatField(required=True)
    meta = {'indexes': ['_id', 'name']}


class SimulationParameters(DynamicDocument):
    temperature = FloatField(required=True)
    target_acceptance = FloatField(required=True)
    continue_sim = BooleanField(default=True)

    iterations = IntField(required=True)
    # target_energy = FloatField(required=True)
    # equilibrium_iterations = IntField(required=True)
    # time_out = FloatField(required=True)

    time = FloatField(required=True)
    meta = {'indexes': ['temperature']}


class Calc(DynamicDocument):
    name = StringField(required=True)
    kwargs = DictField(required=True)


class PES(DynamicDocument):
    name = StringField(required=True)
    calc_list = ListField(required=True)


class Simulation(DynamicDocument):
    # Simulation Request Part, all the inputs for a simulation
    name = StringField(required=True)
    params = ReferenceField(SimulationParameters, reverse_delete_rule=DENY,
                            required=True,
                            db_field='params_id')
    atoms = ReferenceField(AtomicConfig, reverse_delete_rule=DENY,
                           required=True,
                           db_field='atoms_id')
    pes = ReferenceField(PES, reverse_delete_rule=DENY, required=True,
                         db_field='PES_id')

    # Simulation returns
    start_energy = FloatField()
    final_energy = FloatField()
    start_time = FloatField()
    end_time = FloatField()
    traj_file_uid = StringField()
