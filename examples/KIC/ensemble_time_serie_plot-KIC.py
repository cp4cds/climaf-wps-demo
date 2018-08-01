#!/bin/python

# --------------------------------------------------------------------------------------------------
# -- Interfacing the script with CliMAF: writing a command line taking arguments
# -- The associated CliMAF operation is:
#    cscript('ensemble_plot','python ensemble_plot.py --filenames="${mmin}" --outfig=${out} --labels=\'\"${labels}\"\' ', format='png')
# --------------------------------------------------------------------------------------------------

# -- For this, we use the python library argparse
# --------------------------------------------------------------------------------------------------
import argparse

# -- Initialize the parser
# --------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description='Plot script for CliMAF that handles CliMAF ensemble')

# -- Describe the arguments you need 
# --------------------------------------------------------------------------------------------------
# --> filenames = ${ins} in cscript
parser.add_argument('--filenames', action='store', help='Netcdf files provided by CliMAF')
# --> labels = ${labels} (automatically provided by CliMAF in cscript)
parser.add_argument('--labels', action='store', default=None, help='Labels (automatically provided by CliMAF) with ${labels} in cscript')
# --> outfig = ${out}
parser.add_argument('-o','--outfig', action='store', default='fig.png', help='path/filename of the output figure (png)')
parser.add_argument('--variable', action='store', default=None, help='variable')
# --> colors = ${colors}
parser.add_argument('--colors', action='store', default='black', help='colors separated by commas')
parser.add_argument('--experiment', action='store', default=None, help='experiment separated by commas')
parser.add_argument('--leg_colors', action='store', default='black', help='leg_colors separated by commas')
parser.add_argument('--alphas', action='store', default=None, help='alphas separated by commas')
parser.add_argument('--mini', action='store', default=None, help='minimum value')
parser.add_argument('--maxi', action='store', default=None, help='maximum value')
parser.add_argument('--domaine', action='store',default=None, help='domain')
parser.add_argument('--thick', action='store', default=None, help='linethick')
# -- Retrieve the arguments in the script
# --------------------------------------------------------------------------------------------------
#args = parser.parse_args()
args, unknown = parser.parse_known_args()

filenames = args.filenames
outfig = args.outfig
labels = str.replace(args.labels,'"','') # -- We remove the " from labels 
#  -> the string ${labels} provided by CliMAF contains $. If we simply provide a string with $
#     to python, the $ and strings immediately following it are removed it to the string.
#     For instance: label_1$label_2$label_3 will be converted to _1_2_3
#     We thus need to pass '"label_1$label_2$label_3"' instead of label_1$label_2$label_3
#     This explains the specific syntax for labels in the cscript call (example line 5 of this script)
var = args.variable
# Optional: colors
colors = args.colors
experiment = args.experiment
leg_colors = args.leg_colors
alphas=args.alphas
thicks=args.thick
if args.mini: mini=float(args.mini)
if args.maxi: maxi=float(args.maxi)
domaine=args.domaine

# -- We cut the strings to do python lists
# --------------------------------------------------------------------------------------------------
filenames_list = str.split(filenames,' ')
labels_list    = str.split(labels,'$')
colors_list    = str.split(colors,',')

#if len(colors_list)==1: colors_list = colors_list*len(filenames_list)

for filename in filenames_list:
    print 'label: ',labels_list[filenames_list.index(filename)],' ; file:',filename
    #print 'label: ',labels_list[filenames_list.index(filename)],' ; color: ',colors_list[filenames_list.index(filename)],' ; file:',filename
    
# -- Legend
experiment_list = str.split(experiment,',')
leg_colors_list = str.split(leg_colors,',')
alphas_list= str.split(alphas,',')
thicks_list=str.split(thicks,',')
# --------------------------------------------------------------------------------------------------
# -- Plotting (here it's just a dummy plot to produce a result; otherwise CliMAF returns an error
# --------------------------------------------------------------------------------------------------
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from netCDF4 import Dataset
import datetime as dt
import datetime
import matplotlib.dates as mdates

# set the font size globally to get the ticklabels big too:
#mpl.rcParams["font.size"] = 10
# not necessary butyou might want to add options to the figure
fig,ax = plt.subplots()
ax=plt.subplot(111)

#times= pd.date_range(start='1900',periods=201,freq=pd.DateOffset(years=1))
#-- Make a series of dates
start = dt.datetime(1900,1,1,0,0,0)
end = dt.datetime(2100,1,1,0,0,0)
delta = dt.timedelta(days=365)

# Note: "time" is now an array of floats, where 1.0 corresponds
# to one day, and 0.0 corresponds to 1900 (I think...)
# It's _not_ an array of datetime objects!
times = mpl.dates.drange(start, end, delta)
np.shape(times)

i=0
for filename in filenames_list:   
    print filename
    YY=np.empty(201)
    YY[:]=np.nan    
    dataset=Dataset(filename)
    yname=dataset.variables[var].long_name 
    if var == "tas":
        yname=yname+' (degC)'
    if var == "tos":
        yname=yname+' (degC)'
    if var == "pr":
        yname=yname+' (mm/day)'
    if var == "uas":
        yname=yname+' (m/S)'
    y=dataset.variables[var][:,0,0]
    a=np.size(y)
    
    if a == 87:
       for j in range(0,86):
           YY[j+30]=y[j]
            
    if a == 32:
       for j in range(0,31):
           YY[j+(1979-1900)]=y[j]
    
    if a == 111:
       for j in range(0,110):
           YY[j]=y[j]

    if a == 106:   
       for j in range(0, 105):
           YY[j]=y[j]

    if a == 95:
       for j in range(0,94):
           YY[j+106]=y[j]

    #plt.xlabel=('time')
    #plt.ylabel=(yname)
    plt.plot(times,YY,colors_list[i],alpha=float(alphas_list[i]),linewidth=float(thicks_list[i]))   
    if args.mini and args.maxi:
        plt.ylim(mini,maxi)
    plt.xlim(datetime.datetime(1900,1,1,0,0,0),datetime.datetime(2100,1,1,0,0,0))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=240))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xlabel('time',fontsize=10)
    plt.ylabel(yname,fontsize=10)
    plt.grid(True)
    i=i+1
    plt.gcf().autofmt_xdate() 
    plt.title("Yearly temporal evolution of "+yname+" \n"+domaine+" mean",fontsize=10)    
      
from PIL import Image    
import matplotlib.lines as line

#JS#l0 = line.Line2D([], [], color=leg_colors_list[0], linestyle='-', label=experiment_list[0])
#JS#l1 = line.Line2D([], [], color=leg_colors_list[1], label=experiment_list[1]) 
#JS#l2 = line.Line2D([], [], color=leg_colors_list[2], label=experiment_list[2])  
#JS#l5 = line.Line2D([], [], color=leg_colors_list[3], label=experiment_list[5]) 
l0 = line.Line2D([], [], color=leg_colors_list[0], linestyle='-', label=experiment_list[0])
l1 = line.Line2D([], [], color=leg_colors_list[1], label=experiment_list[1]) 
l2 = line.Line2D([], [], color=leg_colors_list[2], label=experiment_list[2])  
#JS#l5 = line.Line2D([], [], color=leg_colors_list[3], label=experiment_list[5]) 
#JS#plt.legend(handles=[l0,l1,l2,l5],loc=0,ncol=2)
plt.legend(handles=[l0,l1,l2],loc=0,ncol=1)
# -- Save the plot (using the ${out} value provided by CliMAF)
# -------------------------------------------------------------------------------------------------
plt.savefig(outfig)
print outfig
import shutil 
import os
import os.path
src_file=outfig
#dir_dst = "/home/util1/KIC/figures"
#out_file="Atlas_"+var+"_time_series_"+domaine+"_new.png"
#dst_file = os.path.join(dir_dst, out_file)
#shutil.copyfile(src_file, dst_file)

