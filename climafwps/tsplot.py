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

    Arguments:
      model:       climate model ID [string]
      experiment:  experiment name [string]
      start_year:  4-digit start year [string or integer]
      end_year:    4-digit end year [string or integer]
      variable:    variable ID [string]
      output:      output file name [string]

    Return: plot object
    """
    # Set data location to CMIP5 archive on local file system
    cmip5_path = configuration.get_config_value("data", "archive_root")
    LOGGER.info("CMIP5 data path: %s", cmip5_path)
    dataloc(project="CMIP5", organization="CMIP5_DRS", url=[cmip5_path])
    # Define a dataset selection from the CMIP5 project, using user inputs
    dset = ds(project='CMIP5', model=model, experiment=experiment, frequency='monthly',
              period='{}-{}'.format(start_year, end_year), variable=variable)
    # Calculate the spatial average
    gmean = space_average(dset)
    # Generate the time series plot object
    p = plot(gmean, title='Global mean time series of CMIP5: {}, {}, {}'.format(
             variable, model, experiment),
             format='png')
    # Write the plot to the output file and return it
    cfile(p, target=output)
    return p
