import coronacaster

data = coronacaster.get_data_from_eu()
coronacaster.fit('Finland', data, startdate='2020-04-01')
# coronacaster.fit('Finland', data, ftype='exp')
coronacaster.plot_country('Finland', data)

