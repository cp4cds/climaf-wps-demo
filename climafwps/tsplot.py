"""
generate global mean timeseries
===============================

Holds function to generate a plot of a global mean time series
from CMIP5.
"""

import os
import tempfile
from pywps import configuration

import logging
LOGGER = logging.getLogger('PYWPS')

# init climaf
os.environ['CLIMAF_CACHE'] = os.path.join(tempfile.gettempdir(), 'climaf_cache')
from climaf.api import ds, cfile, plot, space_average
from climaf.dataloc import dataloc


def create_global_mean_ts_plot(model, experiment, start_year, end_year, variable,
                               output='output.png'):
    """
    Create a global average time series of CMIP5 variable and plot to output.
    """
    cmip5_path = configuration.get_config_value("data", "archive_root")
    LOGGER.info("CMIP5 data path: %s", cmip5_path)
    dataloc(project="CMIP5", organization="CMIP5_DRS", url=[cmip5_path])
    dset = ds(project='CMIP5', model=model, experiment=experiment, frequency='monthly',
              period='{}-{}'.format(start_year, end_year), variable=variable)
    gmean = space_average(dset)

    p = plot(gmean, title='Global mean time series of CMIP5: {}, {}, {}'.format(
             variable, model, experiment),
             format='png')
    cfile(p, target=output)
    return p
