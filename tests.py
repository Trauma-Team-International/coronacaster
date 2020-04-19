import coronacaster

data = coronacaster.get_eu_data()
coronacaster.fit('Finland', data)
