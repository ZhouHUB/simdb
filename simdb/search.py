from simdb.odm_templates import AtomicConfig
from filestore import commands as fsc
from filestore.api import register_handler

# register_handler('csv', CSVLineHandler)

__author__ = 'christopher'


def find_atomic_config_document(**kwargs):
    atomic_configs = AtomicConfig.objects(__raw__=kwargs).order_by('-_id')
    for atomic_config in atomic_configs:
        # may need 'ase' in here somewhere
        atomic_config.file_payload = fsc.retrieve(atomic_config.file_uid)
    return atomic_configs

