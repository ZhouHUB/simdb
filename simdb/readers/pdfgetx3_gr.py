import math
import numpy as np


def load_gr_file(gr_file=None, skiplines=None, rmin=None, rmax=None, **kwargs):
    """
    Load gr files produced from PDFgetx3
    """
    exp_keys = ['qmax', 'qbin', 'qmin', 'rmin', 'rmax', 'rstep']
    if skiplines is None:
        with open(gr_file) as f:
            exp_dict = {}
            lines = f.readlines()
            record = False
            for num, line in enumerate(lines, 1):
                if "# End of config" in line:
                    record = False
                if record is True and line.startswith(tuple(exp_keys)):
                    # print 'line = ', line
                    key, val = line.split(' = ')
                    if key in exp_keys:
                        exp_dict[key] = float(val)
                if '# PDF calculation setup' in line:
                    record = True
                if '#### start data' in line:
                    skiplines = num + 2
                    break
    data = np.loadtxt(gr_file, skiprows=skiplines)
    r = data[:-1, 0]
    gr = data[:-1, 1]
    if rmax is not None:
        r = r[:math.ceil(rmax / exp_dict['rstep'])]
        gr = gr[:math.ceil(rmax / exp_dict['rstep'])]
        exp_dict['rmax'] = rmax

    if rmin is not None:
        r = r[math.ceil(rmin / exp_dict['rstep']):]
        gr = gr[math.ceil(rmin / exp_dict['rstep']):]
        exp_dict['rmin'] = rmin
    exp_dict['sampling'] = 'full'
    return r, gr, exp_dict