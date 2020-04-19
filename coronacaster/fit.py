def fit(country,
        data,
        ftype='poly1',
        samples=10000,
        startdate=None,
        enddate=None,
        limit=0,
        **kwargs):
    
    """
    do monte carlo fit of posterior (gives also the point max estimate)

    :param country:  Country name, if there is "countries" column in the data - else use "World or "" for all data
    :param data: dataframe with "dates" (datetime) and "cases" columns - coses is the number of daily new cases
    :param ftype:  'polyN' where N is a number between 0 and a few (don't try more than 10 or so - becomes quite slow)
                or  'exp'  for exponential
    :param samples: number of samples to use
    :param startdate: start date number
    :param enddate: end date number
    :param limit: take start date to be where cumulative count exceeds limit
    :param **kwargs: model params if wanted to use
    :return: fitresults
    """
    
    import pymc3 as pm
    import datetime
    import pandas as pd

    from .utils import calculateStats, modelfit_eval
    from .models import poly_model, exp_model
    
    if isinstance(startdate, str):
        startdate = pd.to_datetime(startdate)

    if country=="World" or country=="all" or len(country)==0:
        temp = data.sort_values('dates')
    
    else:
        temp = data[data.countries == country].sort_values('dates')

    if startdate == None:
        startdate = temp[temp.cases > limit].dates.dt.date.min()
    
    if enddate == None:
        enddate = temp[temp.cases > 0].dates.dt.date.max()
    
    print('date range: ', startdate, enddate)
    
    temp_new = temp[(temp.dates.dt.date>=startdate) & (temp.dates.dt.date<=enddate)]

    try:
        x0 = temp_new.dates.dt.date - startdate
    except:
        x0 = temp_new.dates - startdate

    x = x0.dt.days
    y = temp_new.cases.cumsum().values

    print('Number of data points: ', x.shape[0])  # , y.shape[0])

    log = 'lin'
    
    if ftype=='exp':
        model, varnames, modelfun = exp_model(x, y, **kwargs)
        log = 'log'
    
    elif 'poly' in ftype:
        order = int(ftype[4:])
        model, varnames, modelfun = poly_model(x, y, order, **kwargs)
    
    else:
        print('undefined model - %s'%type)
        return None

    with model:
        step = pm.Slice()
        trace = pm.sample(samples, step=step)  # , step, tune=2500, cores=10)

    varstats = []
    print()
    for va in varnames + ['sigma']:
        stats = calculateStats(trace[va])  # mean 2, std 3, 20% 5, 80% 7
        print('model variable  "%s"  has mean:'%va, stats[2], ', std:', stats[3], ', 20%-80%:', stats[5:8:2])
        varstats.append([stats[2], stats[3], stats[5], stats[7]])

    sigma = sum(calculateStats(trace['sigma'])[2:4])  # mean + std

    plotstrs = ['%s COVID-19 cases %s model'%(country, ftype),
                '%s to %s'%(datetime.datetime.strftime(startdate, '%d.%m.%Y'),
                            datetime.datetime.strftime(enddate, '%d.%m.%Y')),
                'cumulative cases']
    modelfit_eval(y, x, modelfun, varstats[0:-1], sigma=sigma,
                                plotstrs=plotstrs, log=log, varnames=varnames)

    return trace