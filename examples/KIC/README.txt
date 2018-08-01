# KIC Demo

I've set up an example based on a practical Sebastien and Hugo Dayan gave last week for the KIC Climate.

Here is the protocole:

1. I assume that you've correctly set up your site_settings (in $CLIMAF/climaf/site_settings.py) and used it to set up the cmip5 project in $CLIMAF/climaf/projects/cmip5.py (as we've already exchanged on this)

2. Get the KIC_latest.gz and put it in a working directory; in the KIC/ directory, you will find:
- two notebooks that will produce:
** a plot of the temporal evolution of a variable over the historical period and for the RCP 2.6 and 8.5 scenarios (CMIP5_Time_series_KIC.ipynb)
** a plot of the map of the difference between a user-chosen period in the RCP 8.5 scenario and a historical period (Map_RCP85_projections_KIC.ipynb)
** in both notebooks, you can choose to do the plot among a selection of variables, and either for a selection of models, or for all available CMIP5 models (across the different experiments)
- two pythons scripts: KIC_functions.py and ensemble_time_series_plot-KIC.py; the notebooks use those scripts

You will need the following python packages: pandas, PIL, matplotlib, mpl_toolkit and basemap (don't remember whether the last one comes with mpl_toolkit... worth giving it a check).
