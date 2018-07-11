from pywps import Process, LiteralInput, LiteralOutput
from pywps.app.Common import Metadata


class TimeSeriesPlot(Process):
    def __init__(self):
        inputs = [
            LiteralInput('delay', 'Delay between every update',
                         default='10', data_type='float')
        ]
        outputs = [
            LiteralOutput('sleep_output', 'Sleep Output', data_type='string')
        ]

        super(Sleep, self).__init__(
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
        import time

        if 'delay' in request.inputs:
            sleep_delay = request.inputs['delay'][0].data
        else:
            sleep_delay = 10

        time.sleep(sleep_delay)
        response.update_status('PyWPS Process started. Waiting...', 20)
        response.outputs['sleep_output'].data = 'done sleeping'

        return response
