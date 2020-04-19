import coronacaster

data = coronacaster.get_data_from_eu()
coronacaster.forecast('Finland', data, startdate='2020-04-01')
# coronacaster.forecast('Finland', data, ftype='exp')
coronacaster.plot_country('Finland', data)

