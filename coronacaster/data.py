def get_data_from_eu():

    import pandas as pd

    source = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx'

    data = pd.read_excel(source)
    
    cols = data.columns.tolist()
    cols[0] = 'dates'
    cols[6] = 'countries'

    data.columns = cols
    
    return data