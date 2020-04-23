def calculateStats(DataSeries, mode=None):
    """
    Ignores nan's
    :param DataSeries: column of a dataframe
    :return: a 9-length vector with 0-min,1-max,2-mean,3-stddev,4-10%-percentile,
                5-20%percentile,6-median,7-80%percentile,8-90%percentile
    """

    import numpy as np
    import datetime

    if mode == 'cols':
        return 'min','max','mean','stddev','10%-percentile','20%percentile','median','80%percentile','90%percentile'

    data = np.array(DataSeries).astype(np.float)
    output = np.empty(9)
    output[0] = data.min()
    output[1] = data.max()
    output[2] = np.nanmean(data)
    output[3] = np.nanstd(data)
    output[4] = np.nanpercentile(data, 10)
    output[5] = np.nanpercentile(data, 20)
    output[6] = np.nanpercentile(data, 50)
    output[7] = np.nanpercentile(data, 80)
    output[8] = np.nanpercentile(data, 90)
    
    return output


def modelfit_eval_dates(data, x, dates, modelfun, varstats, varnames=[], target=None, sigma=None, plotstrs=None, log='lin'):
    """
    evaluates the goodness of the model fit to the data
    -- need a predition option or separate function
    :param data: data to compare data to
    :param x: data points
    :param dates:  data points as datetime.date values
    :param modelfun: function of the model of (params[0:N], data)
    :param varstats: variable stats of 2,3,5,7 from Pandas_utilities.calculateStats(), namely mean, std, 20% and 80%
    :param varnames: variable names
    :param target: x value for a preditiction point
    :param sigma: one variation from mean value fit
    :param plotstrs: plotting strings as a list of title, xlabel, ylabel
    :return:
    """

    import numpy as np
    import pandas as pd

    import datetime
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import seaborn as sns

    x = np.asarray(x)
    data = np.asarray(data)

    # model fit mean parameters
    param_means = np.asarray([par[0] for par in varstats])
    modelmean = modelfun(param_means, x)

    # correlation coefficient
    corr = np.corrcoef(modelmean, data)[0][1]

    datalen = len(data)
    difference = modelmean - data
    meandiff = sum(np.abs(difference))/datalen
    L2norm = np.linalg.norm(difference)
    maxposdifference = max(0, max(difference))
    maxnegdifference = min(0, min(difference))

    idx = ['corr', 'mean_diff', 'norm_of_diff', 'max_pos_diff', 'max_neg_diff']
    metrics = [corr, meandiff, L2norm, maxposdifference, maxnegdifference]
    df = pd.DataFrame({corr},index=['corr'])
    for ii, ind2 in enumerate(idx):
        df.loc[ind2]=metrics[ii]

    # plot
    fig = plt.figure(figsize=[12, 8])  #
    ax1 = fig.add_subplot(111)  # category percentage

    ax1.plot_date(dates, data, 'k^-', linewidth=1.5, markersize=4, label='truth', color='#005082', alpha=.5)

    # target
    pred=0
    if not (target == None):
        targetdate = min(dates) + datetime.timedelta(days=target)
        if targetdate>max(dates): #a prediction
            dates=pd.date_range(start=min(dates),end=targetdate+datetime.timedelta(days=1))
            x = np.arange(0,target+2)
            modelmean=modelfun(param_means, x)
            fitTarget = modelfun(param_means, target)
            df.loc['prediction']=fitTarget
            pred=1
        else: # targetdate is where data exists
            fitTarget = modelfun(param_means, target)
            df.loc['target_fit']=fitTarget
    ax1.plot_date(dates, modelmean, 'bo-', linewidth=1, markersize=4, label='best fit', color='#FF1053', alpha=.5)
    
    if not('lin' in log):
        plt.yscale(log)

    if not (sigma==None):
        ax1.fill_between(dates, modelmean - sigma, modelmean + sigma, facecolor='#00a8cc', alpha=0.2, label='+/- sigma')

    # additional CI's:
    if len(varnames) > 0:
        facecols = ['#ffa41b', '#333333', '#666666', '#999999', '#CCCCCC', '#EEEEEE']
        facecols = facecols[:len(varnames)]
        #facecols.reverse()
        err_low=[]
        err_upp=[]
        for vi in range(len(varstats)):
            # using variance of variable #vi and others mean values
            vi_var = varstats[vi][2:4]
            means_temp = param_means.copy()
            means_temp[vi] = vi_var[0]
            fit1 = modelfun(means_temp, x)
            if not (target == None):
                err_low.append(fitTarget-modelfun(means_temp,target))
            means_temp[vi] = vi_var[1]
            fit2 = modelfun(means_temp, x)
            ax1.fill_between(dates, fit1, fit2, alpha=0.2, facecolor=facecols[vi % 8],
                     label='var %s variance' % varnames[vi])
            if not (target == None):
                err_upp.append(modelfun(means_temp,target)-fitTarget)

        if not(target==None):
            err_low.sort()
            err_upp.sort()
            if len(err_low)<2 or sigma>err_low[1]: # > second smallest
                err_low.append(sigma)
                err_upp.append(sigma)
            err_low=err_low[1:] #drop smallest
            err_upp=err_upp[1:]
            yerr= np.array([np.prod(err_low)**(1/len(err_low)),np.prod(err_upp)**(1/len(err_upp))])
            yerr.shape = (-1, 1)
            if pred:
                df.loc['prediction_CI_low'] = yerr[0]
                df.loc['prediction_CI_high'] = yerr[1]

    else:
        # all variance combined: (assuming 80% add to the same direction and 20% likewise -- otherwise you can switch them)
        param_80 = np.asarray([par[3] for par in varstats])
        modelmax = modelfun(param_80, x)
        param_20 = np.asarray([par[2] for par in varstats])
        modelmin = modelfun(param_20, x)

        ax1.fill_between(dates, modelmin, modelmax, alpha=0.5, facecolor='grey', label='all parameter variance')

    if not(target==None):
        ax1.errorbar(targetdate, fitTarget, yerr=yerr, fmt='ko', ecolor='k', capthick=0, elinewidth=2, label='prediction')

    ax1.legend()
    if not (plotstrs == None):
        plt.title(plotstrs[0])
        plt.xlabel(plotstrs[1])
        plt.ylabel(plotstrs[2])

    ax1.xaxis.set_major_locator(ticker.AutoLocator())
    ax1.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax1.xaxis.set_tick_params(labelsize=10)
    
    plt.title(label=plotstrs[0], fontsize=20)
    plt.xlabel('dates', fontsize=12, labelpad=8)
    plt.ylabel('cumulative cases', fontsize=12, labelpad=8)

    ax1.tick_params(axis='both', which='major', pad=8)

    sns.despine()

    return df


def poly_fun(x, y):
    """
    function x[0] + x[1]*y + x[2]*y**2 + ...
    :param x: parameters
    :param y: datapoints
#    :param order: polynomial order  - we get this from the length of x
    :return: result
    """
    ret = 0
    for oi in range(len(x)):
        ret += x[oi] * y **oi
    return ret