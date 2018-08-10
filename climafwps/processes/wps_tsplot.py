import os.path

from pywps import Process, LiteralInput, ComplexOutput
from pywps import Format
from pywps.app.Common import Metadata

from climafwps import util

ALLOWED_VALUES = {
    'model':
        'ACCESS1-0 ACCESS1-3 bcc-csm1-1 bcc-csm1-1-m BNU-ESM CanCM4 '
        'CanESM2 CCSM4 CESM1-BGC CESM1-CAM5 CESM1-WACCM CMCC-CM CMCC-CMS '
        'CNRM-CM5 CSIRO-Mk3-6-0 EC-EARTH FGOALS-g2 FIO-ESM GFDL-CM2p1 '
        'GFDL-CM3 GFDL-ESM2G GFDL-ESM2M GISS-E2-H GISS-E2-H-CC GISS-E2-R '
        'GISS-E2-R-CC HadCM3 HadGEM2-AO HadGEM2-CC HadGEM2-ES inmcm4 '
        'IPSL-CM5A-LR IPSL-CM5A-MR IPSL-CM5B-LR MIROC4h MIROC5 MIROC-ESM '
        'MIROC-ESM-CHEM MPI-ESM-LR MPI-ESM-MR MRI-CGCM3 NorESM1-M NorESM1-ME'.split(),
    'experiment':
        'rcp45 rcp60 rcp8 historical'.split(),
    'variable':
        'cl clt evspsbl hur huss prc ps rldscs rlutcs rsdt '
        'rsut sci tas tauu ua vas cli clw hfls hurs '
        'mc prsn psl rlus rsds rsus rsutcs sfcWind tasmax '
        'tauv uas wap clivi clwvi hfss hus pr prw rlds rlut '
        'rsdscs rsuscs sbl ta tasmin ts va zg'.split()
}


class TimeSeriesPlot(Process):
    def __init__(self):
        inputs = [
            LiteralInput('model', 'Model',
                         abstract="Climate model ID",
                         default='HadGEM2-ES', data_type='string',
                         allowed_values=ALLOWED_VALUES['model']),
            LiteralInput('experiment', 'Experiment',
                         abstract="Experiment name",
                         default='rcp45', data_type='string',
                         allowed_values=ALLOWED_VALUES['experiment']),
            LiteralInput('variable', 'Variable',
                         abstract="Variable ID",
                         default='tas', data_type='string',
                         allowed_values=ALLOWED_VALUES['variable']),
            LiteralInput('start_year', 'Start Year',
                         abstract="4-digit start year",
                         default='2010', data_type='integer'),
            LiteralInput('end_year', 'End Year',
                         abstract="4-digit end year",
                         default='2020', data_type='integer'),
        ]
        outputs = [
            ComplexOutput('output', 'Output plot',
                          abstract='Generated timeseries plot.',
                          as_reference=True,
                          supported_formats=[Format('image/png')])
        ]

        super(TimeSeriesPlot, self).__init__(
            self._handler,
            identifier='tsplot',
            version='1.1.0',
            title='CMIP5 Global Mean Time Series',
            abstract='Uses the CliMAF tool to calculate a time series of global mean values'
                     ' for a variable, model, experiment and ensemble member from the CMIP5 archive.'
                     ' The time series is plotted as a line graph showing change '
                     ' in the global mean value against time.',
            profile='',
            metadata=[
                Metadata('CliMAF', 'http://climaf.readthedocs.io/en/latest/'),
                Metadata('Documentation',
                         'https://climaf-wps-demo.readthedocs.io/en/latest/processes.html#tsplot',
                         role=util.WPS_ROLE_DOC),
                Metadata('Media',
                         'https://climaf-wps-demo.readthedocs.io/en/latest/_static/media/tsplot_thumbnail.png',
                         role=util.WPS_ROLE_MEDIA),
            ],
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        from climafwps import tsplot
        response.update_status('Plotting ...', 0)
        # output in workdir
        output_filename = os.path.join(self.workdir, 'output.png')
        # start tsplot
        tsplot.create_global_mean_ts_plot(
            model=request.inputs['model'][0].data,
            experiment=request.inputs['experiment'][0].data,
            start_year=request.inputs['start_year'][0].data,
            end_year=request.inputs['end_year'][0].data,
            variable=request.inputs['variable'][0].data,
            output=output_filename)
        # store result
        response.outputs['output'].file = output_filename
        # done
        response.update_status('Plotting done', 100)
        return response
