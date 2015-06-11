from simdb.odm_templates import *
from filestore import commands as fsc
from filestore.api import register_handler
from .utils import _ensure_connection

__author__ = 'christopher'

@_ensure_connection
def find_atomic_config_document(**kwargs):
    atomic_configs = AtomicConfig.objects(__raw__=kwargs).order_by('-_id').all()
    for atomic_config in atomic_configs:
        atomic_config.file_payload = fsc.retrieve(atomic_config.file_uid)
        yield atomic_config


@_ensure_connection
def find_pdf_data_document(**kwargs):
    pdf_data_sets = PDFData.objects(__raw__=kwargs).order_by('-_id').all()
    for data_set in pdf_data_sets:
        data_set.file_payload = fsc.retrieve(data_set.file_uid)
        yield data_set
