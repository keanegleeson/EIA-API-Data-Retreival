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
url = 'https://api.eia.gov/category/?api_key=9efbf856649057f0dc4c8269b27d938c&category_id=476337'

category_ids = ['476337']

# r = requests.get(url)
# json_data = r.json()
# category = json_data.get('category')
# # print(category)
# child_series = category.get('childseries')
# # print(child_series)
# child_categories = category.get('childcategories')
# # print(child_categories)

# # excluding first item in list since it's all fuels
# for i in child_categories[1:]:
#     category_ids.append(str(i.get('category_id')))

# print(category_ids)

# lets go by region
# Pacific, Mountain, West South Central, West North Central, South Atlantic, Middle Atlantic, New England, West North Central, East North Central
# These are the data that will be excluded in the case of state renewables


# get the series for each category
child_series = []
series_ids = []
series_names = []
final_data = []


substring = 'M'  # Change to A for Annual, Q for quarterly

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

print(series_ids)
# # going through the list of all monthly series ids and only picking the regional ones to create data table


for i in range(len(series_ids)):
    url = 'http://api.eia.gov/series/?api_key=' + \
        api_key + '&series_id=' + series_ids[i]
    print(url)
    r = requests.get(url)
    json_data = r.json()
    series_name = json_data.get('series')[0]["name"]
    series_id = json_data.get('series')[0]["series_id"]
    series_units = json_data.get('series')[0]["units"]
    source_name = json_data.get('series')[0]["description"]
    df = pd.DataFrame(json_data.get('series')[0].get('data'),
                      columns=['Date', 'Volume'])
    df.set_index('Date', drop=True, inplace=True)
    df['Set Name'] = source_name
    df['Unit'] = series_units
    final_data.append(df)

imports = pd.concat(final_data)


imports.to_excel(
    "G:\\Advanced Visualization\\Staging\\Common\\Keane\\NG_Imports.xlsx")
