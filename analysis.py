""" 
--Environment--
.venv\Scripts\activate.ps1
--Run Command--
& c:/Users/mickh/OneDrive/01_Developer/02_Python/20220802/.venv/Scripts/python.exe -i `
c:/Users/mickh/OneDrive/01_Developer/02_Python/20220802/analysis.py
"""
import pandas_profiling
import pandas as pd
analysis = {}
datasets = {}
def load_datasets():
    datasets['hierarchy_0'] = (
        pd.read_csv('sample-item-hierarchy.csv')
        )[['HIERARCHYLEVEL1_ID', 'HIERARCHYLEVEL1_NAME','HIERARCHYLEVEL2_NAME'
        ,'HIERARCHYLEVEL3_NAME','HIERARCHYLEVEL4_NAME']]
    datasets['items_0'] = (
        pd.read_csv('samples-item-data.csv')
        )[['itemcode', 'hierarchylevel1_id']]
    datasets['sales_0'] = (
        pd.read_csv('sample-sales-data.csv')
        #WeightedItemFlag Always =  No
        )[['SalesDate','SalesHour','StoreID','ItemCode', 'SalesQuantity', 'SalesValue']]
   
def prepare_datasets():
    datasets['item_hierarchy'] = pd.merge(
        datasets['items_0']
        , datasets['hierarchy_0']
        , left_on = 'hierarchylevel1_id', right_on = 'HIERARCHYLEVEL1_ID'
    )
    datasets['sales_1'] = pd.merge(
        datasets['sales_0']
        , datasets['item_hierarchy']
        , left_on = 'ItemCode', right_on = 'itemcode'
    )    

    datasets['sales_1']['SalesDatetime'] = pd.to_datetime(datasets['sales_1']['SalesDate']) + pd.to_timedelta(datasets['sales_1']['SalesHour'], unit='H')


analysis['LVL4_Sales'] = datasets['sales_1'][['SalesDatetime', 'HIERARCHYLEVEL4_NAME', 'SalesQuantity', 'SalesValue']]
analysis['LVL4_Sales'].plot.line(subplots=True)

def generate_profiles():
    for k,v in datasets.items():
        profile = pandas_profiling.ProfileReport(v)
        profile.to_file(f'{k}.html')

"""
datasets['sales']['SalesDate'].max() == 2017-06-30 00:00:00.000
datasets['sales']['SalesDate'].min() == 2017-06-01 00:00:00.000

SalesHour between 1-23

50 Stores
112992 Items

16146754 Items Sold
$77,762,379.35 of items sold

"""

