import pandas as pd  # Used to create and manipulate data tables
import requests  # used to access EIA API
# import re #using to parse strings for field names
# the below libraries were copied over from medium post, probably not needed for my purposes
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
import matplotlib.ticker as ticker

# http://api.eia.gov/category/?api_key=9efbf856649057f0dc4c8269b27d938c&category_id=1
# API Key from EIA
api_key = '9efbf856649057f0dc4c8269b27d938c'

# get all the different fuel type category ids
url = 'http://api.eia.gov/category/?api_key=9efbf856649057f0dc4c8269b27d938c&category_id=3'

category_ids = []

r = requests.get(url)
json_data = r.json()
category = json_data.get('category')
# print(category)
child_series = category.get('childseries')
# print(child_series)
child_categories = category.get('childcategories')
# print(child_categories)

# excluding first item in list since it's all fuels
for i in child_categories[1:]:
    category_ids.append(str(i.get('category_id')))

# print(category_ids)

# lets go by region
# Pacific, Mountain, West South Central, West North Central, South Atlantic, Middle Atlantic, New England, West North Central, East North Central
#These are the data that will be excluded in the case of state renewables
regions = ['PCC', 'MTN', 'WSC', 'WNC', 'SAT', 'MAT', 'NEW', 'WNC', 'ENC','ESC','PCN']

# get the series for each category
child_series = []
series_ids = []
series_names = []
final_data = []


substring = 'A'  # Change to A for Annual, Q for quarterly

# going through each category id and getting each series within the category id(source)
for i in category_ids:
    url = 'http://api.eia.gov/category/?api_key=' + \
        api_key + '&category_id=' + i
    # print(url)

    r = requests.get(url)
    json_data = r.json()
    category = json_data.get('category')
    child_series = category.get('childseries')
    # going through each series
    for i in child_series:
        last_letter = i.get('series_id')[-1]
        # print(last_letter)
        if substring in last_letter:
            series_ids.append(i.get('series_id'))


# going through the list of all monthly series ids and only picking the regional ones to create data table
for i in range(len(series_ids)):
    # print(series_ids[i])
    if any(ele in series_ids[i] for ele in regions):
        pass

    else:
        url = 'http://api.eia.gov/series/?api_key=' + \
            api_key + '&series_id=' + series_ids[i]
        r = requests.get(url)
        json_data = r.json()
        series_name = json_data.get('series')[0]["name"]
        series_id = json_data.get('series')[0]["series_id"]
        series_name_list = series_name.split(" : ")
        series_id_list = series_id.split("-")
        # getting rid of messy total on end of region name field
        state_name = series_id_list[1]
        source_name = series_name_list[1]

        df = pd.DataFrame(json_data.get('series')[0].get('data'),
                          columns=['Date', 'Generation'])
        df.set_index('Date', drop=True, inplace=True)
        df['Source'] = source_name
        df['State'] = state_name
        final_data.append(df)

state_elec = pd.concat(final_data)


state_elec.to_excel(
    "G:\\Advanced Visualization\\Staging\\Common\\Keane\\EIA_electricity_generation_by_region_by_generation_type_annual_by_state.xlsx")
