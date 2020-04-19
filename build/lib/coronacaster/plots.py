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

    if country=='all' or country=='World' or len(country)==0:
        temp = data.sort_values('dates')
    else:
        temp = data[data.countries == country].sort_values('dates')
    if temp.shape[0]==0:  # check that country exists in data
        print('Country %s not found in data'%country)
        # countries = temp.countriesAndTerritories.unique()
        print(sorted(data.countries.unique()))
        return

    # check that there are none zero values in cases
        # if start == None:
    first_date2 = next((ti['dates'] for ind, ti in temp.iterrows() if ti['cases'] > limit), None)
    if first_date2 == None:
        print('no cumulative cases over the limit %f for country '%limit, country)
        return
    if not(start is None):
        first_date2 = max(start, first_date2)
    # country = 'Finland'  # Italy
    temp = temp[temp.dates>= first_date2]
    if end is None:
        end = temp.dates.max()
        print('date range with non-zero data: \n', first_date2, '-', end)
    else:
        print('date range with non-zero data: \n', first_date2, '-', end)
        temp = temp[temp.date <= end]

    fig, ax = plt.subplots()
    plt.plot_date(temp.dates, temp.cases.cumsum().values, 'o-', label='cases')
    plt.plot_date(temp.dates, temp.deaths.cumsum().values, 'o-', label='deaths')
    if log == "log":
        ax.set_yscale('log')

    fig.autofmt_xdate()
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    plt.title(country+' Cases and Deaths')
    plt.legend()

    return first_date2 if first_date2 is not None else None