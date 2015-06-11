from simdb.odm_templates import AtomicConfig
from filestore import commands as fsc
from filestore.api import register_handler
from .utils import _ensure_connection
# register_handler('csv', CSVLineHandler)

__author__ = 'christopher'

@_ensure_connection
def find_atomic_config_document(**kwargs):
    atomic_configs = AtomicConfig.objects(__raw__=kwargs).order_by('-_id').all()
    ret = []
    for atomic_config in atomic_configs:
        # may need 'ase' in here somewhere
        atomic_config.file_payload = fsc.retrieve(atomic_config.file_uid)
        yield atomic_config
    #     ret.append(atomic_config)
    # return ret

