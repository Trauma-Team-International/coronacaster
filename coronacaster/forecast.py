def forecast(country,
             data,
             ftype='poly1',
             samples=10000,
             startdate=None,
             enddate=None,
             limit=0,
             targetdate=None,
             tune=2000,
             chains=20,
             cpu_cores=4,
             return_inis=False,
             **kwargs):
    
    """
    do monte carlo fit of posterior (gives also the point max estimate)

    :param country:  Country name, if there is "countries" column in the data - else use "World or "" for all data
    :param data: dataframe with "dates" (datetime) and "cases" columns - coses is the number of daily new cases
    :param ftype:  'polyN' where N is a number between 0 and a few (don't try more than 10 or so - becomes quite slow)
                or  'exp'  for exponential
    :param samples: number of samples to use
    :param startdate: start date of the data to use as datetime.date
    :param enddate: end date of the data to use as datetime.date
    :param limit: take start date to be where cumulative count exceeds limit
    :param targetdate: datetime.date for prediction
        import datetime
        targetdate = datetime.datetime.strptime('2020-06-30','%Y-%m-%d').date()
    :param return_inis: don't run but return initial parameters
    :param **kwargs: model params if wanted to use like intercept=[int_mean,int_std]
    :return: fitresults
    """
    
    import pymc3 as pm
    import datetime
    import pandas as pd

    from .utils import calculateStats, modelfit_eval_dates
    from .models import poly_model, exp_model, logistic_model
    
    if isinstance(startdate, str):
        startdate = pd.to_datetime(startdate)

    if country=="World" or country=="all" or len(country)==0:
        temp = data.sort_values('dates')
        temp['cases'] = temp.groupby(['dates'])['cases'].transform('sum')
        temp['deaths'] = temp.groupby(['dates'])['deaths'].transform('sum')
        temp.drop_duplicates(subset=['dates'], inplace=True)
    
    else:
        temp = data[data.countries == country].sort_values('dates')

    temp['cumcases']=temp.cases.cumsum().values
    if startdate == None:
        startdate = temp[temp.cumcases > limit].dates.dt.date.min()

    if enddate == None:
        enddate = temp[temp.cases > 0].dates.dt.date.max()
    
    temp_new = temp[(temp.dates.dt.date>=startdate) & (temp.dates.dt.date<=enddate)]
    intercept = next((value for key, value in kwargs.items() if key == 'intercept'), None)
    if intercept is None:
        intercept = temp_new.cumcases.values.min()
        kwargs['intercept'] = [intercept, intercept / 10 + 20]

    try:
        x0 = temp_new.dates.dt.date - startdate
    except:
        x0 = temp_new.dates - startdate

    x = x0.dt.days
    y = temp_new.cumcases.values

    if targetdate == None:
        xTarget = None
    else:
        xTarget = (targetdate - startdate).days

    log = 'lin'
    
    if ftype=='exp':
        slope = next((value for key, value in kwargs.items() if key == 'slope'), None)
        if slope is None:
            a10 = (y.max() - y[0]) / x.max()
            kwargs['slope'] = [a10 / 2, a10 / 4 + 10]
        if return_inis:
            return kwargs
        model, varnames, modelfun = exp_model(x, y, **kwargs)
        log = 'log'
    
    elif 'poly' in ftype:
        order = int(ftype[4:])
        a1 = next((value for key, value in kwargs.items() if key == 'a1'), None)
        if not a1:
            a10 = (y.max() - y[0]) / x.max()
            kwargs['a1'] = [a10, a10 / 4 + 20]
        if return_inis:
            return kwargs
        model, varnames, modelfun = poly_model(x, y, order, **kwargs)

    elif 'logis' in ftype or 'scurve' in ftype or 'sigmoid' in ftype:
        peak = next((value for key, value in kwargs.items() if key == 'peak'), None)
        if peak is None:
            peak0 = y.max() * 1.5
            kwargs['peak'] = [peak0, peak0 / 4]
        shifted = next((value for key, value in kwargs.items() if key == 'shifted'), None)
        if shifted is None:
            kwargs['shifted'] = [x[temp.cases.idxmax()], x.max() / 5]
        if return_inis:
            return kwargs
        model, varnames, modelfun = logistic_model(x, y, **kwargs)
    else:
        return None

    with model:
        step = pm.Slice()
        trace = pm.sample(samples, step=step, tune=tune, chains=chains, cores=cpu_cores)  # , step, tune=2500, cores=10)

    varstats = []
    for va in varnames + ['sigma']:
        stats = calculateStats(trace[va])  # mean 2, std 3, 20% 5, 80% 7
        varstats.append([stats[2], stats[3], stats[5], stats[7]])

    sigma = sum(calculateStats(trace['sigma'])[2:4])  # mean + std

    plotstrs = ['%s COVID-19 cases %s model'%(country, ftype),
                '%s to %s'%(datetime.datetime.strftime(startdate, '%d.%m.%Y'),
                            datetime.datetime.strftime(enddate, '%d.%m.%Y')),
                'cumulative cases']
    df = modelfit_eval_dates(y, x, temp_new.dates,
                       modelfun,
                       varstats[0:-1],
                       sigma=sigma,
                       target=xTarget,
                       plotstrs=plotstrs,
                       log=log,
                       varnames=varnames)

    for va in varnames + ['sigma']:
        stats = calculateStats(trace[va])
        df.loc[va + '_mean'] = stats[2]
        df.loc[va + '_std'] = stats[3]
        #df.loc[va + '_20%'] = stats[5]
        #df.loc[va + '_80%'] = stats[7]

    return df