"""
generate global mean timeseries
===============================

Holds function to generate a plot of a global mean time series
from CMIP5.
"""

import os
import tempfile

# init climaf
os.environ['CLIMAF_CACHE'] = os.path.join(tempfile.gettempdir(), 'climaf_cache')
from climaf.api import ds, cfile, plot, space_average


def create_global_mean_ts_plot(model, experiment, start_year, end_year, variable,
                               output='output.png'):
    """
    Create a global average time series of CMIP5 variable and plot to output.
    """
    dset = ds(project='CMIP5', model=model, experiment=experiment, frequency='monthly',
              period='{}-{}'.format(start_year, end_year), variable=variable)
    gmean = space_average(dset)

    p = plot(gmean, title='Global mean time series of CMIP5: {}, {}, {}'.format(
             variable, model, experiment),
             format='png')
    cfile(p, target=output)
    return p
