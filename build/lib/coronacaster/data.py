def get_data_from_eu():

    import pandas as pd

    source = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'

    data = pd.read_csv(source)
    
    cols = data.columns.tolist()
    cols[0] = 'dates'
    cols[6] = 'countries'

    data.columns = cols
    data['dates'] = pd.to_datetime(data['dates'])
    
    return data