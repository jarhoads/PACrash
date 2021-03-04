'''
Clean crash datasets and merge them into a file for analysis
'''

import pandas as pd
from collections import defaultdict
from functools import reduce

# def select_vars():
#     '''
#     return a dictionary with subsets of the dataframe for analysis
#     the subsets will be lists of column names to filter the dataframe
#     '''

#     keep = defaultdict(list)

#     # create lists of data columns to keep from each file
#     keep['crash'] = ['CRN', 'DISTRICT', 'COUNTY', 'MUNICIPALITY', 'POLICE_AGCY', 
#              'CRASH_YEAR', 'CRASH_MONTH', 'DAY_OF_WEEK', 'TIME_OF_DAY', 
#              'HOUR_OF_DAY', 'ILLUMINATION', 'WEATHER', 'ROAD_CONDITION',
#              'COLLISION_TYPE', 'RELATION_TO_ROAD', 'INTERSECT_TYPE', 'TCD_TYPE', 
#              'LOCATION_TYPE', 'URBAN_RURAL', 'FATAL_COUNT', 'INJURY_COUNT', 
#              'PERSON_COUNT', 'LATITUDE', 'LONGITUDE', 
#              'EST_HRS_CLOSED', 'LANE_CLOSED', 'LN_CLOSE_DIR',
#              'NTFY_HIWY_MAINT', 'VEHICLE_COUNT', 'AUTOMOBILE_COUNT', 
#              'MOTORCYCLE_COUNT', 'BUS_COUNT', 'SMALL_TRUCK_COUNT', 'HEAVY_TRUCK_COUNT', 
#              'SUV_COUNT', 'VAN_COUNT', 'BICYCLE_COUNT', 'MAJ_INJ_COUNT', 
#              'MOD_INJ_COUNT', 'MIN_INJ_COUNT',
#              'TOT_INJ_COUNT', 'DRIVER_COUNT_16YR', 
#              'DRIVER_COUNT_17YR', 'DRIVER_COUNT_18YR', 'DRIVER_COUNT_19YR', 'DRIVER_COUNT_20YR', 
#              'DRIVER_COUNT_50_64YR', 'DRIVER_COUNT_65_74YR', 'DRIVER_COUNT_75PLUS', 'UNBELTED_OCC_COUNT', 
#              'UNB_DEATH_COUNT', 'UNB_MAJ_INJ_COUNT', 'BELTED_DEATH_COUNT', 'BELTED_MAJ_INJ_COUNT', 
#              'MCYCLE_DEATH_COUNT', 'MCYCLE_MAJ_INJ_COUNT', 'BICYCLE_DEATH_COUNT', 'BICYCLE_MAJ_INJ_COUNT', 
#              'PED_COUNT', 'PED_DEATH_COUNT', 'PED_MAJ_INJ_COUNT', 'MAX_SEVERITY_LEVEL', 
#              'COMM_VEH_COUNT', 'DEC_LAT', 'DEC_LONG']

#     keep['person'] = ['CRN', 'PERSON_TYPE', 'INJ_SEVERITY', 'AGE', 'SEX', 'DVR_LIC_STATE']
    
#     # keep['vehicle'] = ['CRN', 'BODY_TYPE', 'DAMAGE_IND', 'GRADE', 
#     #                    'IMPACT_POINT', 'INS_CO', 'MAKE_CD', 'MODEL_CD', 'VEH_TYPE',
#     #                    'MODEL_YR', 'PARTIAL_VIN', 'PEOPLE_IN_UNIT', 'RDWY_ALIGNMENT']
    
#     keep['roadway'] = ['CRN', 'ROUTE', 'SEGMENT', 'SPEED_LIMIT', 'STREET_NAME', 'RDWY_SEQ_NUM']

#     keep['flag'] = ['CRN', 'INJURY_OR_FATAL', 'FATAL_OR_MAJ_INJ', 'INJURY', 'FATAL', 
#                     'ALCOHOL_RELATED', 'DRINKING_DRIVER', 'UNBELTED', 'DRUG_RELATED', 
#                     'ILLEGAL_DRUG_RELATED', 'DRUGGED_DRIVER', 'IMPAIRED_DRIVER']

#     return keep

def create_df(file_name, vars_name):

    # read the data file into a dataframe
    df_data = pd.read_csv(file_name, engine='python')

    #select_df_vars = select_vars()
    #df_vars = select_df_vars[vars_name]

    #return df_data[df_vars]
    return df_data

def merge_dfs(left, right):
    return pd.merge(left, right, on='CRN')

def create_crash_df(crash_file, roadway_file, flag_file):

    data_info = [(crash_file, 'crash'), (flag_file, 'flag'), (roadway_file, 'roadway')]

    merge_frames = [create_df(f_name, variables) for f_name, variables in data_info]
    crash_df = reduce(merge_dfs, merge_frames)

    return crash_df[(crash_df['RDWY_SEQ_NUM'] == 3)]

    # return butler_df[(butler_df['COUNTY'] == 10) & (butler_df['RDWY_SEQ_NUM'] == 3)]