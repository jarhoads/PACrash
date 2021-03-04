'''
Data Exploration Module for Pennsylvania Crash Data from Butler County
Joshua Rhoads 2019
'''

import pandas as pd
import numpy as np
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from scipy.stats import chi2_contingency


def read_crash_data():
        #FILE_NAME = r'data\butler_full_clean.csv'
        FILE_NAME = r'data2\butler_crash_analysis.csv'
        data = pd.read_csv(FILE_NAME, engine='python')
        return data
        
    #FILE_NAME = r'data\ButlerCounty2015Edit.csv'
#     FILE_NAME = r'data\butler_2007_2017.csv'
        

def keep_vars():
    '''
    keep_df will return a dictionary with subsets of the dataframe for analysis
    the subsets will be lists of column names to filter the dataframe
    '''
    # df = read_crash_data()

    keep = defaultdict(list)

    # create lists of data
    keep['numeric'] = ['PERSON_COUNT', 'FATAL_COUNT', 'INJURY_COUNT', 'VEHICLE_COUNT', 'AUTOMOBILE_COUNT',
                       'MOTORCYCLE_COUNT', 'BUS_COUNT', 'SMALL_TRUCK_COUNT', 'HEAVY_TRUCK_COUNT',
                       'SUV_COUNT', 'VAN_COUNT', 'EST_HRS_CLOSED']
    
    keep['categorical'] = ['CRN', 'ALCOHOL_RELATED_FULL', 'CRASH_YEAR', 'CRASH_MONTH', 'DAY_OF_WEEK',  
                           'HOUR_OF_DAY', 'ILLUMINATION_FULL', 'WEATHER_FULL', 'ROAD_CONDITION_FULL',
                           'COLLISION_TYPE_FULL', 'INTERSECT_TYPE_FULL',
                           'LOCATION_TYPE_FULL', 'URBAN_RURAL',  'ROUTE', 'RDWY_SEQ_NUM']
                           
    keep['geographic'] = ['LATITUDE', 'LONGITUDE', 'DEC_LAT', 'DEC_LONG']

    return keep

def corr_chart(data):
    corr = data.corr()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(corr,cmap='coolwarm', vmin=-1, vmax=1)
    fig.colorbar(cax)
    ticks = np.arange(0,len(data.columns),1)
    ax.set_xticks(ticks)
    plt.xticks(rotation=90)
    ax.set_yticks(ticks)
    ax.set_xticklabels(data.columns)
    ax.set_yticklabels(data.columns)
    plt.show()

def data_pivot(df, count='CRN', rows='CRASH_MONTH', cols='DAY_OF_WEEK'):
    return pd.pivot_table(df, values=count, index=[rows], columns=[cols], aggfunc=np.count_nonzero)

def heatmap_chart(data, vals='CRN', idx='CRASH_MONTH', cols='DAY_OF_WEEK'):
    df_hm_pivot = pd.pivot_table(data, values=vals, index=[idx], columns=[cols], aggfunc=np.count_nonzero)
    ax = sns.heatmap(df_hm_pivot, linewidth=0.5)
    plt.show()

def boxplots(df, variables, numeric_var):
    fig, ax = plt.subplots(4, 3, figsize=(30, 20))
    for var, subplot in zip(variables, ax.flatten()):
        sns.boxplot(x=var, y=numeric_var, data=df, ax=subplot)

# def clean_route(data):
#     data['ROUTE'].fillna(values=data['STREET_NAME'])
#     return data

def df_hist(df_col):
    df_col.plot.hist(grid=True, bins=20, rwidth=0.9)



