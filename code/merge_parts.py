'''
Uses frames and clean to create a dataset
'''

import pandas as pd
import frames
import clean

def crash_parts_merge(cf, rf, ff):
    ''' return a cleaned and updated dataframe for analysis '''
    crash_df = frames.create_crash_df(crash_file=cf, roadway_file=rf, flag_file=ff)
    #crash_df = clean.clean_nulls(crash_df)
    #crash_df = clean.clean_names(crash_df)

    return crash_df

def save_to_csv(df, save_name):
    df.to_csv(save_name)

