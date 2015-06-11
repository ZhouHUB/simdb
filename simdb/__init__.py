from . import odm_templates
from .odm_templates import DATABASE_ALIAS
import os

connection_config = {'host': 'localhost',
                     'database': 'simdb',
                     'port': 27017,
                     'timezone': 'US/Eastern'}

ATOM_PATH = os.path.join('/mnt/bulk_data/', 'data', 'ase-atoms')
PDF_PATH = os.path.join('/mnt/bulk_data/', 'data', 'PDF')
from . import handlers
