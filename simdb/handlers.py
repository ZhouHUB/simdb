__author__ = 'christopher'
import ase.io as aseio
from ase.io import PickleTrajectory
import os
from pyiid.utils import load_gr_file, build_sphere_np
from pyiid.wrappers.scatter import Scatter
import math


class ASEAtomsHandler(object):
    def __init__(self, filename, diameter=None):
        self.file_type = os.path.splitext(filename)[-1]
        if self.file_type == '.traj':
            self.contents = PickleTrajectory(filename, 'r')
        elif diameter is None:
            self.contents = aseio.read(filename)
        elif diameter is not None:
            self.contents = build_sphere_np(filename, diameter/2.)

    def __call__(self, frame_no=None, *args, **kwargs):
        if frame_no is None:
            # Return the entire trajectory/atomic configuration
            return self.contents

        elif type(frame_no) == tuple and self.file_type == '.traj':
            # Return a chunk of the trajectory
            if len(frame_no) == 3:
                sl = frame_no[2]
            else:
                sl = 1
            return self.contents[frame_no[0]:frame_no[1]:sl]

        elif type(frame_no) == int and self.file_type == 'traj':
            # Return one frame of the trajectory
            return self.contents[frame_no]


class PDFGetX3Handler(object):
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
