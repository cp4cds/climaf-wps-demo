import os.path

from pywps import Process, LiteralInput, ComplexOutput
from pywps import Format
from pywps.app.Common import Metadata

from climafwps import tsplot


class TimeSeriesPlot(Process):
    def __init__(self):
        inputs = [
            LiteralInput('model', 'Model',
                         default='HadGEM2-ES', data_type='string',
                         allowed_values=tsplot.ALLOWED_VALUES['model']),
            LiteralInput('experiment', 'Experiment',
                         default='rcp45', data_type='string',
                         allowed_values=tsplot.ALLOWED_VALUES['experiment']),
            LiteralInput('variable', 'Variable',
                         default='tas', data_type='string',
                         allowed_values=tsplot.ALLOWED_VALUES['variable'])
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
                Metadata('CliMAF', 'https://github.com/senesis/climaf'),
                Metadata('GitHub', 'https://github.com/cp4cds/climaf-wps-demo'),
            ],
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    @staticmethod
    def _handler(request, response):
        response.update_status('Plotting ...', 0)
        # output in workdir
        output_filename = os.path.joing(self.workdir, 'output.png')
        # start tsplot
        tsplot.create_global_mean_ts_plot(
            model=request.inputs['model'][0].data,
            experiment=request.inputs['experiment'][0].data,
            start_year=2010,
            end_year=2020,
            variable=request.inputs['variable'][0].data,
            output=output_filename)
        # store result
        response.outputs['output'].file = output_filename
        # done
        response.update_status('Plotting done', 100)
        return response
