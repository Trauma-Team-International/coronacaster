import datetime, coronacaster, pandas

data = coronacaster.get_data_from_eu()

out = []
countries = data.countries
for country in countries:
  
  # parameters start
  for ftype in ['poly1', 'poly2', 'poly3', 'logis', 'sigmoid', 'scurve']:
    for chain in [20]:
      for sample in [10000]:
        for tune in [2000]:
    
          # do the thing
          temp = coronacaster.forecast(country,
                                     data,
                                     ftype=ftype,
                                     targetdate=datetime.date(2020, 11, 14), cpu_cores=16)

          # make record of the thing
          out.append(temp[0].values)
  
  # save everything
  pandas.DataFrame(out).to_csv('experiment-results.csv')
