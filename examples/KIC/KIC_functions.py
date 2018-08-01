
# # From CMIP5-model selection to the plot of yearly anomalies time series
from climaf.api import *

cscript('ensemble_time_serie_plot','python ensemble_time_serie_plot-KIC.py --filenames=\"${mmin}\" --outfig=${out} --labels=\'\"${labels}\"\' --colors=${colors} --thick=${thick} --variable=${variable} --domaine=\"${domaine}\" --experiment=${experiment} --alphas=${alphas} --leg_colors=${leg_colors} --mini=${mini} --maxi=${maxi}', format='png')

    
def ts_historical_rcps_CMIP5(var, period_hist, period_clim_ref, period_rcps,
                                 title_plot, latmin, latmax, lonmin, lonmax, cmip5_models_list=None, **kwargs):
    # -- General settings
    project_obs = 'ref_ts'
    project = 'CMIP5'
    freq='monthly'
    simu='r1i1p1'
    version='latest'
    
    if var == 'tos':
        period_obs='1900-2010'
        product='NOAA'
        realm='ocean'
    if var == 'pr':
        period_obs='1979-2010' 
        product='GPCP-2.3'
        realm='atmos'
    if var in ['uas','vas','tas','psl']:
        period_obs='1979-2010'
        product='ERAInterim' 
        realm='atmos'
    
    #JS## creation des dictionnaires pour la climatologie de la SST (tos) et des vents de surface (uas,vas)
    #JS#dict_obs = dict(project=project_obs,period=period_obs,variable=var, product=product, frequency=freq)
    #JS#dict_obs_clim = dict(project=project_obs, product = product, variable=var, period=period_clim_ref, frequency=freq)
    #JS##recuperation des donnees observees
    #JS#y=ds(**dict_obs)
    #JS#y_clim=ds(**dict_obs_clim)
    #JS#if var =='pr':
    #JS#    y=ccdo(y,operator='mulc,86400')
    #JS#    y_clim=ccdo(y_clim,operator='mulc,86400')
  
    #JS##regriding 
    #JS#y_regrid=regridll(y,cdogrid="r360x180",latmin=latmin,latmax=latmax,lonmin=lonmin,lonmax=lonmax) 
    #JS#y_clim_regrid=regridll(y_clim,cdogrid="r360x180",latmin=latmin,latmax=latmax,lonmin=lonmin,lonmax=lonmax) 
    #JS##calcul du cycle saisonnier
    #JS#y_clim_seas_regrid = ccdo(y_clim_regrid,operator='-b 64 ymonavg')
    #JS##calcul des moyennes regionales
    #JS#ts_y = space_average(y_regrid)
    #JS#ts_y_clim=space_average(y_clim_seas_regrid)
    #JS#anom_obs =ccdo2(ts_y,ts_y_clim, operator='-b 64 sub')
    #JS#anom_obs=ccdo(anom_obs,operator='-b 64 yearmean')
    
    # -- Build dom
    dom = str(latmin)+','+str(latmax)+','+str(lonmin)+','+str(lonmax)
    
    # creation d'un dictionnaire pour l'historique sur la periode d'etude du 20st = "period_hist" 
    hist_dict = dict(project=project, variable=var, period=period_hist, version = version, simulation=simu,
                     frequency=freq, realm=realm, domain=dom)
    # creation d'un dictionnaire pour les RCPs sur la periode d'etude du 21 st = "period_hist"
    rcp_dict = dict(project=project, variable=var, period=period_rcps, version = version, simulation=simu,
                  frequency=freq, realm=realm, domain=dom)
    #creation d'un dictionnaire sur la periode climatologiqe de reference = "period_clim_ref" afin de calculer les anomalies (cf. 2.)
    hist_dict_clim = dict(project=project, variable=var, period=period_clim_ref, version = version, simulation=simu,
                  frequency=freq, realm=realm, domain=dom)
    #
    if not cmip5_models_list:
        # -- Get all the models available for the historical runs:
        dum_hist_files = str.split( ds(model='*', experiment='historical', **hist_dict).baseFiles(), ' ')

        hist_models = []
        for dum_hist_file in dum_hist_files:
            tmp_model = str.split(os.path.basename(dum_hist_file),'_')[2]
            if tmp_model not in hist_models: hist_models.append(tmp_model)

        # -- Get all the models available for the historical runs:
        dum_rcp26_files = str.split( ds(model='*', experiment='rcp26', **rcp_dict).baseFiles(), ' ')

        rcp26_models = []
        for dum_rcp26_file in dum_rcp26_files:
            tmp_model = str.split(os.path.basename(dum_rcp26_file),'_')[2]
            if tmp_model in hist_models and tmp_model not in rcp26_models: rcp26_models.append(tmp_model)

        # -- Get all the models available for the historical runs:
        dum_rcp85_files = str.split( ds(model='*', experiment='rcp85', **rcp_dict).baseFiles(), ' ')

        rcp85_models = []
        for dum_rcp85_file in dum_rcp85_files:
            tmp_model = str.split(os.path.basename(dum_rcp85_file),'_')[2]
            if tmp_model in rcp26_models and tmp_model not in rcp85_models: rcp85_models.append(tmp_model)

        cmip5_models_list = rcp85_models
    
    print 'Models:'
    print cmip5_models_list
    
    print 'processing CMIP5'
    if var=='tos' or var=='tas':
        whist_dict = hist_dict.copy()
        whist_dict.update(period=hist_dict['period'][0:4])
        offsets_hist = []
        for model in cmip5_models_list:
            dat = ds(model=model, experiment='historical',**whist_dict)
            glob_ave = cMA(space_average(time_average(dat)))[0][0][0]
            if glob_ave < 100.:
                offsets_hist.append(273.15)
            else:
                offsets_hist.append(0.)
            
        wrcp26_dict = rcp_dict.copy()
        wrcp26_dict.update(period=rcp_dict['period'][0:4])
        offsets_rcp26 = []
        for model in cmip5_models_list:
            dat = ds(model=model, experiment='rcp26', **wrcp26_dict)
            glob_ave = cMA(space_average(time_average(dat)))[0][0][0]
            if glob_ave < 100.:
                offsets_rcp26.append(273.15)
            else:
                offsets_rcp26.append(0.)

        wrcp85_dict = rcp_dict.copy()
        wrcp85_dict.update(period=rcp_dict['period'][0:4])
        offsets_rcp85 = []
        for model in cmip5_models_list:
            dat = ds(model=model, experiment='rcp85', **wrcp85_dict)
            glob_ave = cMA(space_average(time_average(dat)))[0][0][0]
            if glob_ave < 100.:
                offsets_rcp85.append(273.15)
            else:
                offsets_rcp85.append(0.)
            
    #creation des ensembles de chacune des experiences
    hist_ens=eds(model=cmip5_models_list, experiment='historical', **hist_dict)
    rcp26_ens=eds(model=cmip5_models_list, experiment='rcp26', **rcp_dict)
    rcp85_ens=eds(model=cmip5_models_list, experiment='rcp85', **rcp_dict)

    #creation des ensembles composes par la periode de reference sur l'historique qui vont servir de reference pour chacune des experiences (historique + RCPs)
    ref_hist_ens=eds(model=cmip5_models_list, experiment='historical', **hist_dict_clim)
  
    #Calcul du cycle saisonnier en mensuel
    clim_hist_ens =ccdo(ref_hist_ens,operator='-b 64 ymonavg')
    
    #calcul des anomalies par rapport a la periode de reference sur l'histoirque 
    diff_hist_dict = dict()
    diff_rcp26_dict = dict()
    diff_rcp85_dict = dict()

    for elt in ref_hist_ens:
        my_diff =ccdo2(hist_ens[elt],clim_hist_ens[elt], operator='-b 64 sub')
        diff_hist_dict[elt] = my_diff
    
    ens_diff_hist = cens(diff_hist_dict, order=cmip5_models_list)

    for elt in rcp26_ens:
        my_diff =ccdo2(rcp26_ens[elt],clim_hist_ens[elt], operator='-b 64 sub')
        diff_rcp26_dict[elt] = my_diff
    
    ens_diff_rcp26 = cens(diff_rcp26_dict, order=cmip5_models_list)

    for elt in rcp85_ens:
        my_diff =ccdo2(rcp85_ens[elt],clim_hist_ens[elt], operator='-b 64 sub')
        diff_rcp85_dict[elt] = my_diff
    
    ens_diff_rcp85 = cens(diff_rcp85_dict, order=cmip5_models_list)
    
    print 'computing spatial mean'  
    ts_hist_ens = ccdo(space_average(ens_diff_hist),operator='-b 64 yearmean')
    ts_rcp26_ens  = ccdo(space_average(ens_diff_rcp26),operator='-b 64 yearmean')
    ts_rcp85_ens  = ccdo(space_average(ens_diff_rcp85),operator='-b 64 yearmean')
    if var =='pr':
        ts_hist_ens=ccdo(ts_hist_ens,operator='mulc,86400')
        ts_rcp26_ens=ccdo(ts_rcp26_ens,operator='mulc,86400')
        ts_rcp85_ens=ccdo(ts_rcp85_ens,operator='mulc,86400')

    print 'construction ensemble final CLIMAF'    

    # -- Pour mettre dans le meme 'objet CliMAF ensemble' les hist, RCPs, il faut rajouter un tag aux noms
    # -- pour les differencier. On le fait ici a la main, en recreant un dictionnaire tot qui va recevoir les resultats
    # -- des hist, RCPs
    tot = dict()

    # -- names est la liste python qui va recevoir les noms avec tags de tous les modeles, et des statistiques
    # --(Ens.Mean, q05 et q95)
    names = []

    #-- Observation
    #JS#name = '.obs'
    #JS#names.append(name)
    #JS#tot.update({name:anom_obs})

    # -- Boucle sur les hist
    for mem in ts_hist_ens:
        name = mem+'.hist'
        names.append(name)
        tot.update({name:ts_hist_ens[mem]})
    # -- Calcul des stats
    tot.update({'Ens.Mean.hist':ccdo_ens(ts_hist_ens,operator='-b 64 ensmean')})
    tot.update({'q95.hist':ccdo_ens(ts_hist_ens,operator='-b 64 enspctl,95')})
    tot.update({'q05.hist':ccdo_ens(ts_hist_ens,operator='-b 64 enspctl,5')})
    names = names + ['q05.hist','q95.hist','Ens.Mean.hist']

    # -- Boucle sur les rcp26
    for mem in ts_rcp26_ens:
        name = mem+'.rcp26'
        names.append(name)
        tot.update({name:ts_rcp26_ens[mem]})
    # -- Calcul des stats
    tot.update({'Ens.Mean.rcp26':ccdo_ens(ts_rcp26_ens,operator='-b 64 ensmean')})
    tot.update({'q95.rcp26':ccdo_ens(ts_rcp26_ens,operator='-b 64 enspctl,95')})
    tot.update({'q05.rcp26':ccdo_ens(ts_rcp26_ens,operator='-b 64 enspctl,5')})
    names = names + ['q05.rcp26','q95.rcp26','Ens.Mean.rcp26']

    # -- Boucle sur les rcp85
    for mem in ts_rcp85_ens:
        name = mem+'.rcp85'
        names.append(name)
        tot.update({name:ts_rcp85_ens[mem]})
    # -- Calcul des stats
    tot.update({'Ens.Mean.rcp85':ccdo_ens(ts_rcp85_ens, operator='-b 64 ensmean')})
    tot.update({'q95.rcp85':ccdo_ens(ts_rcp85_ens,operator='-b 64 enspctl,95')})
    tot.update({'q05.rcp85':ccdo_ens(ts_rcp85_ens,operator='-b 64 enspctl,5')})
    names = names + ['q05.rcp85','q95.rcp85','Ens.Mean.rcp85']

    # -- Construction de l'ensemble CliMAF que l'on va passer a curves() avec la fonction cens()
    tot_ens = cens(tot, order = names)
    cfile(tot_ens)
    
    print 'processing the plot'    
    
    #tmp_colors = ['blueviolet'] + ['lightgrey']*len(time_checked_models_hist) + ['grey','grey','black'] +\
    tmp_colors = ['lightgrey']*len(cmip5_models_list) + ['black','black','black'] +\
                 ['deepskyblue']*len(cmip5_models_list) + ['deepskyblue','deepskyblue','deepskyblue'] +\
                 ['red']*len(cmip5_models_list) + ['red','red','red']
            
    arg_colors = tmp_colors[0]
    for color in tmp_colors[1:len(tmp_colors)]:
        arg_colors+=','+color

    alpha_membre='0.4'
    alpha_percentiles ='0.4'
    alpha_mean='1.'

    #JS#tmp_alphas = ['1.'] + [alpha_membre]*len(time_checked_models_hist) + [alpha_percentiles,alpha_percentiles,alpha_mean] +\
    tmp_alphas = [alpha_membre]*len(cmip5_models_list) + [alpha_percentiles,alpha_percentiles,alpha_mean] +\
                 [alpha_membre]*len(cmip5_models_list) + [alpha_percentiles,alpha_percentiles,alpha_mean] +\
                 [alpha_membre]*len(cmip5_models_list) + [alpha_percentiles,alpha_percentiles,alpha_mean]
    
    arg_alphas = tmp_alphas[0]
    for alpha in tmp_alphas[1:len(tmp_alphas)]:
        arg_alphas+=','+alpha
    
    thick_membre='0.5'
    thick_percentiles='0.5'
    thick_mean='3'
    
    #JS#tmp_thick =  ['3'] + [thick_membre]*len(time_checked_models_hist) + [thick_percentiles,thick_percentiles,thick_mean] +\
    tmp_thick =  [thick_membre]*len(cmip5_models_list) + [thick_percentiles,thick_percentiles,thick_mean] +\
                 [thick_membre]*len(cmip5_models_list) + [thick_percentiles,thick_percentiles,thick_mean] +\
                 [thick_membre]*len(cmip5_models_list) + [thick_percentiles,thick_percentiles,thick_mean]
    
    arg_thick = tmp_thick[0]
    for thick in tmp_thick[1:len(tmp_thick)]:
        arg_thick+=','+thick

    if (not title_plot) or (title_plot.lower()=='global' and dom not in '-90,90,0,360'):
        title_plot = 'Geographical Domain'
    title_plot+=': '+str(lonmin)+'/'+str(lonmax)+'E;'+str(latmin)+'/'+str(latmax)+'N'
    #
    if 'mini' in kwargs and 'maxi' in kwargs:
        minmax = dict(mini=kwargs['mini'], maxi=kwargs['maxi'])
    else:
        minmax = dict()
    result=climaf.operators.ensemble_time_serie_plot(tot_ens,
                                    colors=arg_colors, thick=arg_thick, variable=var,domaine=title_plot,
                                    experiment='historical,rcp26,rcp85',
                                    alphas=arg_alphas, leg_colors='black,deepskyblue,red',
                                    **minmax)
    return result



def plot_projection_map_CMIP5(var, u, v, lonmin=0, lonmax=360, latmin=-90, latmax=90,
                              period_hist='1986-2005', period_rcps = '2081-2100', cmip5_models_list=None):


    GD = str(latmin)+','+str(latmax)+','+str(lonmin)+','+str(lonmax)

    project = 'CMIP5'
    realm = 'atmos'
    if var == 'tos':
        realm = 'ocean'
    realma = 'atmos'  
    freq='monthly'
    #rea=r1i1p1
    version='latest'

    #Historique
    #definition du dictionnaire qui comporte les parametres pour l'historique
    hist_dict= dict(project=project, variable=var, period=period_hist, version = version,
                      frequency=freq, realm=realm, domain=GD)

    hist_dict_u = dict(project=project, variable=u,period=period_hist, version = version,
                      frequency=freq, realm=realma, domain=GD)

    hist_dict_v = dict(project=project, variable=v, period=period_hist, version = version,
                      frequency=freq, realm=realma, domain=GD)

    #RCPs
    #definition du dictionnaire qui comporte les parametres pour les RCPs
    rcp_dict = dict(project=project, variable=var, period=period_rcps, version = version,
                      frequency=freq, realm=realm, domain=GD)
    rcp_dict_u = dict(project=project, variable=u, period=period_rcps, version = version,
                      frequency=freq, realm=realma, domain=GD)
    rcp_dict_v = dict(project=project, variable=v, period=period_rcps, version = version,
                      frequency=freq, realm=realma, domain=GD)
    
    if not cmip5_models_list:
        # -- Get all the models available for the historical runs:
        dum_hist_files = str.split( ds(model='*', experiment='historical', **hist_dict).baseFiles(), ' ')
        hist_models = []
        for dum_hist_file in dum_hist_files:
            tmp_model = str.split(os.path.basename(dum_hist_file),'_')[2]
            if tmp_model not in hist_models: hist_models.append(tmp_model)
        
        dum_hist_files_u = str.split( ds(model='*', experiment='historical', **hist_dict_u).baseFiles(), ' ')
        hist_models_u = []
        for dum_hist_file in dum_hist_files_u:
            tmp_model = str.split(os.path.basename(dum_hist_file),'_')[2]
            if tmp_model not in hist_models_u and tmp_model in hist_models: hist_models_u.append(tmp_model)

        dum_hist_files_v = str.split( ds(model='*', experiment='historical', **hist_dict_v).baseFiles(), ' ')
        hist_models_v = []
        for dum_hist_file in dum_hist_files_v:
            tmp_model = str.split(os.path.basename(dum_hist_file),'_')[2]
            if tmp_model not in hist_models_v and tmp_model in hist_models_u: hist_models_v.append(tmp_model)
                
        # -- Get all the models available for the historical runs:
        dum_rcp85_files = str.split( ds(model='*', experiment='rcp85', **rcp_dict).baseFiles(), ' ')
        rcp85_models = []
        for dum_rcp85_file in dum_rcp85_files:
            tmp_model = str.split(os.path.basename(dum_rcp85_file),'_')[2]
            if tmp_model in hist_models_v and tmp_model not in rcp85_models: rcp85_models.append(tmp_model)

        dum_rcp85_files_u = str.split( ds(model='*', experiment='rcp85', **rcp_dict_u).baseFiles(), ' ')
        rcp85_models_u = []
        for dum_rcp85_file in dum_rcp85_files_u:
            tmp_model = str.split(os.path.basename(dum_rcp85_file),'_')[2]
            if tmp_model in rcp85_models and tmp_model not in rcp85_models_u: rcp85_models_u.append(tmp_model)

        dum_rcp85_files_v = str.split( ds(model='*', experiment='rcp85', **rcp_dict_v).baseFiles(), ' ')
        rcp85_models_v = []
        for dum_rcp85_file in dum_rcp85_files_v:
            tmp_model = str.split(os.path.basename(dum_rcp85_file),'_')[2]
            if tmp_model in rcp85_models_u and tmp_model not in rcp85_models_v: rcp85_models_v.append(tmp_model)

        cmip5_models_list = rcp85_models_v


    print 'Models:'
    print cmip5_models_list

    # Fix a la main: on verifie que le champ de SST est bien en Kelvin; sinon on applique un offset
    if (var == "tos" or var == "tas"):
        whist_dict = hist_dict.copy()
        whist_dict.update(period=hist_dict['period'][0:4])
        offsets_hist = []
        for model in cmip5_models_list:
            dat = ds(model=model, experiment='historical',**whist_dict)
            glob_ave = cMA(space_average(time_average(dat)))[0][0][0]
            if glob_ave < 100.:
                offsets_hist.append(273.15)
            else:
                offsets_hist.append(0.)

        wrcp26_dict = rcp_dict.copy()
        wrcp26_dict.update(period=rcp_dict['period'][0:4])
        offsets_rcp26 = []
        for model in cmip5_models_list:
            dat = ds(model=model, experiment='rcp26', **wrcp26_dict)
            glob_ave = cMA(space_average(time_average(dat)))[0][0][0]
            if glob_ave < 100.:
                offsets_rcp26.append(273.15)
            else:
                offsets_rcp26.append(0.)

        wrcp85_dict = rcp_dict.copy()
        wrcp85_dict.update(period=rcp_dict['period'][0:4])
        offsets_rcp85 = []
        for model in cmip5_models_list:
            dat = ds(model=model, experiment='rcp85', **wrcp85_dict)
            glob_ave = cMA(space_average(time_average(dat)))[0][0][0]
            if glob_ave < 100.:
                offsets_rcp85.append(273.15)
            else:
                offsets_rcp85.append(0.)

    # 2.Calcul de la diff des moyennes d'ensemble RCPs-Hist sur les periodes de ref

    std_dict = dict()
    #calcul de la diff des moyennes d'ensemble RCP26 relativement a 1986-2005
    #Variable
    ens_hist_rcp85=eds(model=cmip5_models_list,experiment='historical',**hist_dict)
    remap_ens_hist_rcp85=regridn(ens_hist_rcp85,cdogrid="r360x180")   
    ens_hist_rcp85_time_average = ccdo(remap_ens_hist_rcp85,operator='timavg')
    Mens_hist_rcp85_time_average = ccdo_ens(ens_hist_rcp85_time_average,operator='ensmean')
    ens_rcp85=eds(model=cmip5_models_list,experiment='rcp85',**rcp_dict)
    remap_ens_rcp85=regridn(ens_rcp85,cdogrid="r360x180")   
    ens_rcp85_time_average = ccdo(remap_ens_rcp85,operator='timavg')
    Mens_rcp85_time_average = ccdo_ens(ens_rcp85_time_average,operator='ensmean')
    diff_rcp85 = fsub(Mens_rcp85_time_average,Mens_hist_rcp85_time_average)
    if var == 'pr':
        diff_rcp85 = ccdo(diff_rcp85,operator='mulc,86400')
        ens_rcp85_time_average= ccdo(ens_rcp85_time_average,operator='mulc,86400')
        ens_hist_rcp85_time_average= ccdo(ens_hist_rcp85_time_average,operator='mulc,86400')

    for elt in ens_hist_rcp85_time_average:
        sub = fsub(ens_rcp85_time_average[elt],ens_hist_rcp85_time_average[elt])
        if var == 'psl':
            sub=fdiv(sub,100)
        std_dict[elt] = sub

    std1 = cens(std_dict,order=cmip5_models_list)
    std = ccdo_ens(std1,operator='ensstd')

    Dat_rcp85=cfile(diff_rcp85)
    std_rcp85=cfile(std)



    std_dict_u = dict()
    #calcul de la diff des moyennes d'ensemble RCP26 relativement a 1986-2005
    #Variable
    ens_hist_rcp85_u=eds(model=cmip5_models_list,experiment='historical',**hist_dict_u)
    remap_ens_hist_rcp85_u=regridn(ens_hist_rcp85_u,cdogrid="r360x180")   
    ens_hist_rcp85_time_average_u = ccdo(remap_ens_hist_rcp85_u,operator='timavg')
    Mens_hist_rcp85_time_average_u = ccdo_ens(ens_hist_rcp85_time_average_u,operator='ensmean')
    ens_rcp85_u=eds(model=cmip5_models_list,experiment='rcp85',**rcp_dict_u)
    remap_ens_rcp85_u=regridn(ens_rcp85_u,cdogrid="r360x180")   
    ens_rcp85_time_average_u = ccdo(remap_ens_rcp85_u,operator='timavg')
    Mens_rcp85_time_average_u = ccdo_ens(ens_rcp85_time_average_u,operator='ensmean')
    diff_rcp85_u = fsub(Mens_rcp85_time_average_u,Mens_hist_rcp85_time_average_u)

    Dat_rcp85_u=cfile(diff_rcp85_u)



    std_dict_v = dict()
    #calcul de la diff des moyennes d'ensemble RCP26 relativement a 1986-2005
    #Variable
    ens_hist_rcp85_v=eds(model=cmip5_models_list,experiment='historical',**hist_dict_v)
    remap_ens_hist_rcp85_v=regridn(ens_hist_rcp85_v,cdogrid="r360x180")   
    ens_hist_rcp85_time_average_v = ccdo(remap_ens_hist_rcp85_v,operator='timavg')
    Mens_hist_rcp85_time_average_v = ccdo_ens(ens_hist_rcp85_time_average_v,operator='ensmean')
    ens_rcp85_v=eds(model=cmip5_models_list,experiment='rcp85',**rcp_dict_v)
    remap_ens_rcp85_v=regridn(ens_rcp85_v,cdogrid="r360x180")   
    ens_rcp85_time_average_v = ccdo(remap_ens_rcp85_v,operator='timavg')
    Mens_rcp85_time_average_v = ccdo_ens(ens_rcp85_time_average_v,operator='ensmean')
    diff_rcp85_v = fsub(Mens_rcp85_time_average_v,Mens_hist_rcp85_time_average_v)

    Dat_rcp85_v=cfile(diff_rcp85_v)



    # 3. Recuperation des champs pour tracer avec Python

    varr=var
    #varr='tos'
    import netCDF4 as nc
    ##DATA
    #Rcp26
    data_rcp85 = nc.Dataset(Dat_rcp85)
    data_rcp85_u = nc.Dataset(Dat_rcp85_u)
    data_rcp85_v = nc.Dataset(Dat_rcp85_v)
    std=nc.Dataset(std_rcp85)
    lat = data_rcp85.variables['lat'][:]
    lon = data_rcp85.variables['lon'][:]
    Z_rcp85 = data_rcp85.variables[varr][0,:,:]
    if var == 'psl':
        Z_rcp85 = Z_rcp85/100
    Z_rcp85_u = data_rcp85_u.variables[u][0,:,:]
    Z_rcp85_v = data_rcp85_v.variables[v][0,:,:]

    Z_std_rcp85= std.variables[varr][0,:,:]
    data_rcp85.close()
    data_rcp85_u.close()
    data_rcp85_v.close()

    std.close()

    # 4. PLOT

    ## 4.1 Importation des modules

    import math
    import matplotlib
    #matplotlib.use('agg')
    matplotlib.use('pdf')
    from mpl_toolkits.basemap import Basemap
    import matplotlib.gridspec as gridspec
    from matplotlib.colors import BoundaryNorm
    from matplotlib.ticker import MaxNLocator
    import numpy as np
    import numpy.ma as ma
    import matplotlib.pyplot as plt
    from pylab import *
    from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
    from mpl_toolkits.axes_grid1.inset_locator import mark_inset

    ## 4.2 Recuperation des coordonnes des valeurs significatives

    np.shape(Z_rcp85)
    YY_lon = []
    YY_lat = []
    lon2=range(len(lon))
    lat2=range(len(lat))
    for j in lon2:
        for i in lat2:
            if abs(Z_rcp85[i,j]) < Z_std_rcp85[i,j]: 
                YY_lon.append(lon[j])   
                YY_lat.append(lat[i])



    #parametres d'entree pour les plots
    #color='RdBu_r'
    if varr == 'pr':
        vmax_div =1
        vmin_div =-1
        color='RdBu'
    if varr in ['tos']: 
        vmax_div =5
        vmin_div =0
        color='Reds'
    if varr in ['tas']: 
        vmax_div =8
        vmin_div =0
        color='Reds'
    if varr == 'psl': 
        vmax_div =3
        vmin_div =-3
        color='RdBu_r'

    lev=MaxNLocator(nbins=8).tick_values(vmin_div, vmax_div)
    m = Basemap(projection='cyl',llcrnrlat=latmin,urcrnrlat=latmax,llcrnrlon=lonmin,urcrnrlon=lonmax,resolution='c',fix_aspect=True)
    U=Z_rcp85_u
    V=Z_rcp85_v
    scale1=1
    width1=1
    dx=6
    dy=6

    fig=plt.figure()

    #PLOT RCP26 
    ax1 =plt.subplot(2,1,1)
    if varr == 'tos':
        ax1.set_title("Sea surface temperature changes in RCP8.5 "+period_rcps+" (relative to "+period_hist+")",fontsize=10)
    if varr == 'tas':
        ax1.set_title("2m air temperature changes in RCP8.5 "+period_rcps+" (relative to "+period_hist+")",fontsize=10)
    if varr == 'pr':
        ax1.set_title("Precipitation changes in RCP8.5 "+period_rcps+" (relative to "+period_hist+")",fontsize=10)
    if varr == 'psl':
        ax1.set_title("",fontsize=10)
    m.drawcoastlines(color = '0.15')
    if varr == 'tos':
        m.fillcontinents(color='w', lake_color=None, ax=None, zorder=None, alpha=None)
    toto=plt.contourf(lon, lat, Z_rcp85, cmap=color,levels=lev, origin="lower",extend='both')

    l1 = YY_lon
    L1 = YY_lat
    x1,y1 = m(l1,L1)
    m.plot(x1,y1,".",markersize=0.000001,color='black')

    q=plt.quiver(lon[::dx], lat[::dy],U[::dy,::dx],V[::dy,::dx])
    qk = plt.quiverkey(q, 0.9, 0.89, 1, r'$1 \frac{m}{s}$', labelpos='E',
                       coordinates='figure')
    
    if lonmax-lonmin < 50: seplon = 10
    if lonmax-lonmin > 50 and lonmax-lonmin <= 200: seplon = 20
    if lonmax-lonmin > 200: seplon = 40
    if latmax-latmin < 50: seplat = 10
    if latmax-latmin > 50: seplat = 20
    
    
    ax1.set_xticks([i for i in range(lonmin,lonmax,seplon)])
    ax1.set_xticklabels([i for i in range(lonmin,lonmax,seplon)])
    ax1.set_yticks([i for i in range(latmin,latmax,seplat)])
    ax1.set_yticklabels([i for i in range(latmin,latmax,seplat)])
    box=ax1.get_position()
    pad,thick=0.002,0.01
    cax=fig.add_axes([ box.xmax + pad, box.ymin, thick,box.height])
    cbar=fig.colorbar(toto,cax=cax)
    if (varr == 'tos'):
        cbar.ax.set_ylabel('degC', fontsize=10)
    if (varr == 'pr'):
        cbar.ax.set_ylabel('mm/day', fontsize=10)    
    if (varr == 'psl'):
        cbar.ax.set_ylabel('hPa', fontsize=10)   





    if varr == 'pr':
        figname = os.getcwd()+'/figures/Precipitation_change_RCP85_'+period_rcps+'_relative_to_'+period_hist+'.pdf'
    if varr == 'tos':
        figname = os.getcwd()+'/figures/Sea_temperature_change_RCP85_'+period_rcps+'_relative_to_'+period_hist+'.pdf'
    if varr == 'tas':
        figname = os.getcwd()+'/figures/2m_air_temperature_change_RCP85_'+period_rcps+'_relative_to_'+period_hist+'.pdf'
    if varr == 'psl':
        figname = os.getcwd()+'/figures/PSL_winds_change_RCP85_'+period_rcps+'_relative_to_'+period_hist+'.pdf'
    
    pngname = str.replace(figname,'pdf','png')
    
    os.system('rm -f '+figname+' '+pngname)
    
    
    plt.savefig(figname, bbox_inches='tight')

    pngname = str.replace(figname,'pdf','png')
    os.system('convert -resize 1000x450! -density 500 '+figname+' '+pngname)

    from IPython.display import Image

    return Image(pngname)
