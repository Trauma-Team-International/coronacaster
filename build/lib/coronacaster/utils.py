#! /usr/bin/env python

# utility functions needed by bayesian fits.py
# # calculateStats()
# # modelfit_eval()
# # poly_fun()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calculateStats(DataSeries):
    """
    Ignores nan's
    :param DataSeries: column of a dataframe
    :return: a 9-length vector with 0-min,1-max,2-mean,3-stddev,4-10%-percentile,
                5-20%percentile,6-median,7-80%percentile,8-90%percentile
    """
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

    print('\n\nMean model vs data: \n  correlation: ', corr,
          '\n mean difference: ', meandiff,
          '\n norm of difference: ', sqrdiff,
          '\n maximum positive difference: ', maxposdifference,
          '\n maximum negative difference: ', maxnegdifference)

    # plot
    fig = plt.figure()  #
    ax1 = fig.add_subplot(111)  # category percentage

    ax1.plot(x, data, 'k^-', linewidth=1.5, markersize=4, label='data')
    ax1.plot(x, modelmean, 'bo-', linewidth=1, markersize=4, label='best fit')
    if not('lin' in log):
        plt.yscale(log)

    if not (sigma==None):
        print('Overall variation in the model: ', sigma)
        ax1.fill_between(x, modelmean - sigma, modelmean + sigma, facecolor='cyan', alpha=0.5, label='+/- sigma')

    # additional CI's:
    if len(varnames) > 0:
        facecols = ['red', 'purple', 'green', 'brown', 'yellow', 'maroon', 'orange', 'pink']
        for vi in range(len(varstats)):
            # using variance of variable #vi and others mean values
            vi_var = varstats[vi][2:4]
            means_temp = param_means.copy()
            means_temp[vi] = vi_var[0]
            print(vi, 'min params', means_temp)
            fit1 = modelfun(means_temp, x)
            means_temp[vi] = vi_var[1]
            print(vi, 'max params', means_temp)
            fit2 = modelfun(means_temp, x)
            ax1.fill_between(x, fit1, fit2, alpha=0.25, facecolor=facecols[vi%8],
                         label='var %s variance'%varnames[vi])

    else:
        # all variance combined: (assuming 80% add to the same direction and 20% likewise -- otherwise you can switch them)
        param_80 = np.asarray([par[3] for par in varstats])
        modelmax = modelfun(param_80, x)
        param_20 = np.asarray([par[2] for par in varstats])
        modelmin = modelfun(param_20, x)

        ax1.fill_between(x, modelmin, modelmax, alpha=0.5, facecolor='grey',
                     label='all parameter variance')

    ax1.legend()
    if not (plotstrs == None):
        plt.title(plotstrs[0])
        plt.xlabel(plotstrs[1])
        plt.ylabel(plotstrs[2])


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