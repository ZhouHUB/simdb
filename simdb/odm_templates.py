"""
ODM templates for use with metadatstore
"""
import os

from mongoengine import DynamicDocument
from mongoengine import (StringField, DictField, IntField, FloatField,
                         ReferenceField, BooleanField, ListField, DENY)

DATABASE_ALIAS = 'simdb'

__all__ = ['AtomicConfig', 'SimulationParameters', 'Calc', 'PES',
           'Simulation']

class PDFData(DynamicDocument):
    name = StringField(required=True)
    data_uid = StringField(required=True)
    experiment_uid = StringField()
    ase_config_id = ReferenceField()
    calc_params = DictField(required=True)
    time = FloatField(required=True)
    meta = {'indexes': ['_id', 'name'], 'db_alias': DATABASE_ALIAS}


class AtomicConfig(DynamicDocument):
    name = StringField(required=False)
    file_uid = StringField(required=True, unique=True)
    time = FloatField(required=True)
    meta = {'indexes': ['_id', 'name'], 'db_alias': DATABASE_ALIAS}


class SimulationParameters(DynamicDocument):
    temperature = FloatField(required=True)
    target_acceptance = FloatField(required=True)
    continue_sim = BooleanField(default=True)

    iterations = IntField(required=True)
    # target_energy = FloatField(required=True)
    # equilibrium_iterations = IntField(required=True)
    # time_out = FloatField(required=True)

    time = FloatField(required=True)
    meta = {'indexes': ['temperature'], 'db_alias': DATABASE_ALIAS}


class Calc(DynamicDocument):
    name = StringField(required=True)
    kwargs = DictField(required=True)
    meta = {'db_alias': DATABASE_ALIAS}


class PES(DynamicDocument):
    name = StringField(required=True)
    calc_list = ListField(required=True)
    meta = {'db_alias': DATABASE_ALIAS}


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
    meta = {'db_alias': DATABASE_ALIAS}
