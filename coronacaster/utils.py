def calculateStats(DataSeries, mode=None):
    """
    Ignores nan's
    :param DataSeries: column of a dataframe
    :return: a 9-length vector with 0-min,1-max,2-mean,3-stddev,4-10%-percentile,
                5-20%percentile,6-median,7-80%percentile,8-90%percentile
    """

    import numpy as np

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


def modelfit_eval(data, x, modelfun, varstats, varnames=[], sigma=None, plotstrs=None, log='lin'):
    """
    evaluates the goodness of the model fit to the data
    -- need a predition option or separate function
    :param data: data to compare data to
    :param x:  data points
    :param modelfun: function of the model of (params[0:N], data)
    :param varstats: variable stats of 2,3,5,7 from Pandas_utilities.calculateStats(), namely mean, std, 20% and 80%
    :param varnames: variable names
    :param sigma: one variation from mean value fit
    :param plotstrs: plotting strings as a list of title, xlabel, ylabel
    :return:
    """

    import numpy as np
    import pandas as pd

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
    meandiff = sum(abs(difference))/datalen
    sqrdiff = np.sqrt(sum([dif**2 for dif in difference]))/datalen
    maxposdifference = max(0, max(difference))
    maxnegdifference = min(0, min(difference))

    idx = ['corr', 'mean_diff', 'norm_of_diff', 'max_pos_diff', 'max_neg_diff']
    df = pd.DataFrame({corr, meandiff, sqrdiff, maxposdifference, maxnegdifference}, index=idx)

    # plot
    fig = plt.figure(figsize=[12, 8])  #
    ax1 = fig.add_subplot(111)  # category percentage

    ax1.plot(x, data, 'k^-', linewidth=1.5, markersize=4, label='truth', color='#005082', alpha=.5)
    ax1.plot(x, modelmean, 'bo-', linewidth=1, markersize=4, label='best fit', color='#FF1053', alpha=.5)
    
    if not('lin' in log):
        plt.yscale(log)

    if not (sigma==None):
        ax1.fill_between(x, modelmean - sigma, modelmean + sigma, facecolor='#00a8cc', alpha=0.2, label='+/- sigma')

    # additional CI's:
    if len(varnames) > 0:
        facecols = ['#ffa41b', '#333333', '#666666', '#999999', '#CCCCCC', '#EEEEEE']
        facecols = facecols[:len(varnames)]
        #facecols.reverse()
        for vi in range(len(varstats)):
            # using variance of variable #vi and others mean values
            vi_var = varstats[vi][2:4]
            means_temp = param_means.copy()
            means_temp[vi] = vi_var[0]
            #print(vi, 'min params', means_temp)
            fit1 = modelfun(means_temp, x)
            means_temp[vi] = vi_var[1]
            #print(vi, 'max params', means_temp)
            fit2 = modelfun(means_temp, x)
            ax1.fill_between(x, fit1, fit2, alpha=0.2, facecolor=facecols[vi%8],
                             label='var %s variance'%varnames[vi])

    else:
        # all variance combined: (assuming 80% add to the same direction and 20% likewise -- otherwise you can switch them)
        param_80 = np.asarray([par[3] for par in varstats])
        modelmax = modelfun(param_80, x)
        param_20 = np.asarray([par[2] for par in varstats])
        modelmin = modelfun(param_20, x)

        ax1.fill_between(x, modelmin, modelmax, alpha=0.5, facecolor='grey', label='all parameter variance')

    ax1.legend()
    if not (plotstrs == None):
        plt.title(plotstrs[0])
        plt.xlabel(plotstrs[1])
        plt.ylabel(plotstrs[2])

    ax1.xaxis.set_major_locator(ticker.AutoLocator())
    ax1.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax1.xaxis.set_tick_params(labelsize=10)
    
    plt.title(label=plotstrs[0], fontsize=20)
    plt.xlabel('days', fontsize=12, labelpad=8)
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