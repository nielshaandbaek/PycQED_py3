# General imports
import time
t0 = time.time()  # to print how long init takes
from importlib import reload  # Useful for reloading while testing
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Qcodes
import qcodes as qc
qc.set_mp_method('spawn')  # force Windows behavior on mac

# Globally defined config
qc_config = {'datadir': '/Users/nader/Develop/notebook/data/',
             'PycQEDdir': '/Users/nader/Develop/qcodes/PycQED_py3/'}


# General PycQED modules
from pycqed.analysis import measurement_analysis as ma
from pycqed.analysis import analysis_toolbox as a_tools
import matplotlib.gridspec as gridspec
from pycqed.utilities import general as gen
# import seaborn.apionly as sns
# sns.set_palette('muted')
# cls = (sns.color_palette())

t1 = time.time()


print('Ran initialization in %.2fs' % (t1-t0))
