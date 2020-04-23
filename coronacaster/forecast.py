def forecast(country,
             data,
             ftype='poly1',
             samples=10000,
             startdate=None,
             enddate=None,
             limit=0,
             intercept=[0,25],
             targetdate=None,
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
    :param targetdate: date number for prediction
    :param **kwargs: model params if wanted to use like intercept=[int_mean,int_std]
    :return: fitresults
    """
    
    import pymc3 as pm
    import datetime
    import pandas as pd

    from .utils import calculateStats, modelfit_eval
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
    if intercept[0]==0:
        intercept[0] = temp_new.cumcases.values.min()
        intercept[1] = intercept[0]/20 + 20

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
        a10 = (y.max() - y[0]) / x.max()
        slope = [a10, a10 / 3 + 10]
        model, varnames, modelfun = exp_model(x, y, intercept=intercept, **kwargs)
        log = 'log'
    
    elif 'poly' in ftype:
        order = int(ftype[4:])
        a10=(y.max() - y[0]) / x.max()
        a1=[a10, a10 / 3 + 20]
        model, varnames, modelfun = poly_model(x, y, order, intercept=intercept, a1=a1, **kwargs)

    elif 'logis' in ftype or 'scurve' in ftype or 'sigmoid' in ftype:
        peak0 = y.max() * 1.5
        peak = [peak0, peak0 / 3]
        model, varnames, modelfun = logistic_model(x, y, intercept=intercept, peak=peak, **kwargs)

    else:
        return None

    with model:
        step = pm.Slice()
        trace = pm.sample(samples, step=step, tune=2000)  # , step, tune=2500, cores=10)

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