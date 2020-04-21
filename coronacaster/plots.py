def plot_country(country, data, log='lin', end=None, start=None, limit=0):
    
    """
    plot the cases of given country
    
    :param country: Country name, if there is "countries" column in the data - else use "World or "" for all data
    :param data: dataframe with "dates" (datetime) and "cases" columns - coses is the number of daily new cases
    :param log: 'log' if logarithmic plot
    :param end:  end datetime to plot x-range
    :param start: start datetime
    :param limit: first date when there is more than given value of cumulative cases
    :return:
    """
    
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import seaborn as sns

    if country=='all' or country=='World' or len(country)==0:
        temp = data.sort_values('dates')
    else:
        temp = data[data.countries == country].sort_values('dates')

    temp['cumcases']=temp.cases.cumsum().values
    temp['cumdeaths']=temp.deaths.cumsum().values
    first_date2 = next((ti['dates'] for ind, ti in temp.iterrows() if ti['cumcases'] > limit), None)
    
    if first_date2 == None:
        #print('no cumulative cases over the limit %f for country '%limit, country)
        return
    
    if not(start is None):
        first_date2 = max(start, first_date2)
    
    temp = temp[temp.dates>= first_date2]
    if end is None:
        end = temp.dates.max()
        #print('date range with non-zero data: \n', first_date2, '-', end)
    else:
        #print('date range with non-zero data: \n', first_date2, '-', end)
        temp = temp[temp.date <= end]

    fig, ax = plt.subplots(figsize=[12, 8])
    plt.plot_date(temp.dates, temp.cumcases.values, '', linewidth=3.5, label='cases', color='#005082', alpha=.5)
    plt.plot_date(temp.dates, temp.cumdeaths.values, '', linewidth=3, label='deaths', color='#FF1053', alpha=.5)


    if log == "log":
        ax.set_yscale('log')

    fig.autofmt_xdate()
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.xaxis.set_tick_params(labelsize=10)
    plt.title(country + ': Cases and Deaths', fontsize=20)
    plt.xlabel('', fontsize=12, labelpad=8)
    plt.ylabel('total', fontsize=12, labelpad=8)
    plt.legend()

    ax.tick_params(axis='both', which='major', pad=8)

    sns.despine()

    return first_date2
