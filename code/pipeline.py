'''
Data Pipeline Module for Pennsylvania Crash Data from Butler County
Joshua Rhoads 2019
'''

import merge_parts
import merge_frames


DATA_FILES = [{'crash':  r'data\CRASH_2007_E.csv', 'roadway': r'data\ROADWAY_2007_E.csv', 'flag': r'data\FLAG_2007_E.csv'},
              {'crash':  r'data\CRASH_2008_E.csv', 'roadway': r'data\ROADWAY_2008_E.csv', 'flag': r'data\FLAG_2008_E.csv'},
              {'crash':  r'data\CRASH_2009_E.csv', 'roadway': r'data\ROADWAY_2009_E.csv', 'flag': r'data\FLAG_2009_E.csv'},
              {'crash':  r'data\CRASH_2010_E.csv', 'roadway': r'data\ROADWAY_2010_E.csv', 'flag': r'data\FLAG_2010_E.csv'},
              {'crash':  r'data\CRASH_2011_E.csv', 'roadway': r'data\ROADWAY_2011_E.csv', 'flag': r'data\FLAG_2011_E.csv'},
              {'crash':  r'data\CRASH_2012_E.csv', 'roadway': r'data\ROADWAY_2012_E.csv', 'flag': r'data\FLAG_2012_E.csv'},
              {'crash':  r'data\CRASH_2013_E.csv', 'roadway': r'data\ROADWAY_2013_E.csv', 'flag': r'data\FLAG_2013_E.csv'},
              {'crash':  r'data\CRASH_2014_E.csv', 'roadway': r'data\ROADWAY_2014_E.csv', 'flag': r'data\FLAG_2014_E.csv'},
              {'crash':  r'data\CRASH_2015_E.csv', 'roadway': r'data\ROADWAY_2015_E.csv', 'flag': r'data\FLAG_2015_E.csv'},
              {'crash':  r'data\CRASH_2016_E.csv', 'roadway': r'data\ROADWAY_2016_E.csv', 'flag': r'data\FLAG_2016_E.csv'},
              {'crash':  r'data\CRASH_2017_E.csv', 'roadway': r'data\ROADWAY_2017_E.csv', 'flag': r'data\FLAG_2017_E.csv'}]

def pipeline_merge_parts():
    ''' Return a list of dataframes from merged data tables '''
    return [merge_parts.crash_parts_merge(year['crash'], year['roadway'], year['flag']) for year in DATA_FILES]

def pipeline_save_parts(df_list):
    ''' Save a csv file for each year from a list of dataframes '''

    file_list = []
    for i, df_i in enumerate(df_list):
        data_name = r'data\CRASH_' + str(2007+i) + '_df.csv'
        file_list.append(data_name)
        merge_parts.save_to_csv(df_i, data_name)
    
    return file_list

def pipeline_merge_years(df_files):
    ''' Return a dataframe after merging dataframes from a list into one '''
    return merge_frames.merge_dfs(df_files)
