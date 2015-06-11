__author__ = 'christopher'
import ase.io as aseio
import ase
import os
import math

from filestore.api import register_handler
from filestore.handlers import HandlerBase


class ASEAtomsHandler(HandlerBase):
    specs = {'ase'} | HandlerBase.specs

    def __init__(self, filename):
        self.filename = str(filename)

    def __call__(self, is_trajectory):
        if is_trajectory:
            return ase.io.PickleTrajectory(self.filename, 'r')
        else:
            return ase.io.read(self.filename)


class PDFGetX3Handler(HandlerBase):
    specs = {'pdfgetx3'} | HandlerBase.specs

    def __init__(self, filename):
        self.contents = load_gr_file(filename)

    def __call__(self, rmin=None, rmax=None, *args, **kwargs):
        r, gobs, exp = self.contents
        if rmax is not None:
            exp['rmax'] = rmax
            r = r[:math.ceil(rmax/exp['rstep'])]
            gobs = gobs[:math.ceil(rmax/exp['rstep'])]
        if rmin is not None:
            exp['rmin'] = rmin
            r = r[math.ceil(rmin/exp['rstep']):]
            gobs = gobs[math.ceil(rmin/exp['rstep']):]

        s = Scatter(exp)

        return r, gobs, exp, s


handlers = [ASEAtomsHandler, PDFGetX3Handler]
for handler in handlers:
    for spec in handler.specs:
        register_handler(spec, handler)
