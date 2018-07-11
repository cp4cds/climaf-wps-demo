"""
generate global mean timeseries
===============================

Holds function to generate a plot of a global mean time series
from CMIP5.
"""

from climaf.api import ds, cfile, plot


_ALLOWED_VALUES = {
    'model':
        'ACCESS1-0 ACCESS1-3 bcc-csm1-1 bcc-csm1-1-m BNU-ESM CanCM4 '
        'CanESM2 CCSM4 CESM1-BGC CESM1-CAM5 CESM1-WACCM CMCC-CM CMCC-CMS '
        'CNRM-CM5 CSIRO-Mk3-6-0 EC-EARTH FGOALS-g2 FIO-ESM GFDL-CM2p1 '
        'GFDL-CM3 GFDL-ESM2G GFDL-ESM2M GISS-E2-H GISS-E2-H-CC GISS-E2-R '
        'GISS-E2-R-CC HadCM3 HadGEM2-AO HadGEM2-CC HadGEM2-ES inmcm4 '
        'IPSL-CM5A-LR IPSL-CM5A-MR IPSL-CM5B-LR MIROC4h MIROC5 MIROC-ESM '
        'MIROC-ESM-CHEM MPI-ESM-LR MPI-ESM-MR MRI-CGCM3 NorESM1-M NorESM1-ME'.split(),
    'experiment':
        'rcp45 rcp60 rcp8'.split(),
    'variable':
        'cl clt evspsbl hur huss prc ps rldscs rlutcs rsdt '
        'rsut sci tas tauu ua vas cli clw hfls hurs '
        'mc prsn psl rlus rsds rsus rsutcs sfcWind tasmax '
        'tauv uas wap clivi clwvi hfss hus pr prw rlds rlut '
        'rsdscs rsuscs sbl ta tasmin ts va zg'.split()
}


def create_global_mean_ts_plot(model, experiment, start_year, end_year, variable,
                               output='output.png'):
    """
    Create a global average time series of CMIP5 variable and plot to output.
    """
    # Validate arguments
    assert(model in _ALLOWED_VALUES['model'])
    assert(experiment in _ALLOWED_VALUES['experiment'])
    assert(variable in _ALLOWED_VALUES['variable'])

    dset = ds(project='CMIP5', model=model, experiment=experiment, frequency='monthly',
              period='{}-{}'.format(start_year, end_year), variable=variable)
    gmean = space_average(dset)

    p = plot(gmean, title='Global mean time series of CMIP5: {}, {}, {}'.format(
             variable, model, experiment),
             format='png')
    cfile(p, target=output)
    return p


if __name__ == '__main__':
    create_global_mean_ts_plot('HadGEM2-ES', 'rcp45', 2010, 2020, 'tas', 'output.png')
