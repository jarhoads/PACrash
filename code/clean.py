'''
Data Cleaning Module for Pennsylvania Crash Data from Butler County
Joshua Rhoads 2019
'''

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from scipy.stats import chi2_contingency


def clean_nulls(df):
    ''' returns a dataframe with null values imputed '''

    clean_values = {'SPEED_LIMIT': 0, 'STREET_NAME':'UNKNOWN', 
                     'BODY_TYPE':'UNKNOWN', 'DAMAGE_IND':'UNKNOWN',
                     'GRADE': 'N', 'IMPACT_POINT': 99, 
                     'SEGMENT': 'UNKNOWN', 'EST_HRS_CLOSED': 0}

    filled_df = df.fillna(clean_values)
    filled_df['ROUTE'] = filled_df['ROUTE'].fillna(value=filled_df['STREET_NAME'])

    return filled_df

def clean_names(df):
    ''' returns a dataframe with names corrected '''

    clean_names = {'WEATHER': {1: 'Clear', 2: 'Rain', 3: 'Sleet or Hail', 
                               4: 'Snow', 5: 'Fog', 6: 'Rain and Fog',
                               7: 'Sleet and Fog', 8: 'Other', 9: 'Unknown'},
                   'ILLUMINATION': {1: 'Daylight', 2: 'Dark - No Street Lights', 3: 'Dark - Street Lights',
                                    4: 'Dusk', 5: 'Dawn', 6: 'Dark - Unknown Lighting',
                                    8: 'Other', 9: 'Unknown'},
                    'ROAD_CONDITION': {0: 'Dry', 1: 'Wet', 2: 'Sand/Mud/Dirt/Oil/Gravel', 3: 'Snow Covered',
                                       4: 'Slush', 5: 'Ice', 6: 'Ice Patches',
                                       7: 'Water', 8: 'Other', 9: 'Unknown'},
                    'COLLISION_TYPE': {0: 'Non Collision', 1: 'Rear-End', 2: 'Head-On', 3: 'Backing',
                                       4: 'Angle', 5: 'Sideswipe (Same Dir)', 6: 'Sideswipe (Opposite Dir)',
                                       7: 'Hit Fixed Object', 8: 'Hit Pedestrian', 9: 'Other/Unknown'},
                    'MAX_SEVERITY_LEVEL': {0: 'Not Injured', 1: 'Fatal Injury', 2: 'Serious Injury', 3: 'Minor Injury',
                                       4: 'Possible Injury', 8: 'Injury - Unknown', 9: 'Unknown'},
                    'INTERSECT_TYPE': {0: 'Mid-Block', 1: 'Four-Way Intersection', 2: 'T-Intersection', 
                                       3: 'Y-Intersection', 4: 'Traffic Circle/Roundabout', 5: 'Multi-leg Intersection',
                                       6: 'On-Ramp', 7: 'Off-Ramp', 8: 'Crossover', 9: 'Railroad Crossing',
                                       10: 'Other', 99: 'Unknown'},
                    'LOCATION_TYPE': {0: 'Not Applicable', 1: 'Underpass', 2: 'Ramp', 
                                      3: 'Bridge', 4: 'Tunnel', 5: 'Toll Booth',
                                      6: 'Crossover Related', 7: 'Driveway or Parking Lot', 8: 'Ramp or Bridge', 
                                      9: 'Unknown'},
                    # 'MAKE_CD': {'01': 'American Motors', '02': 'Jeep-Willys-Kaiser', '03': 'AM General',
                    #             '6': 'Chrysler','7': 'Dodge', '8': 'Imperial', 
                    #             '9': 'Plymouth', '10': 'Eagle', '12': 'Ford', 
                    #             '13': 'Lincoln', '14': 'Mercury', '18': 'Buick/Opel',
                    #             '19': 'Cadillac', '20': 'Chevrolet', '21': 'Oldsmobile',
                    #             '22': 'Pontiac', '23': 'GMC', '24': 'Saturn', 
                    #             '25': 'Grumman', '29': 'Other Domestic', '30': 'Volkswagen', 
                    #             '31': 'Alfa Romero', '32': 'Audi', '33': 'Austin/Healey', 
                    #             '34': 'BMW', '35': 'Nissan-Datsun', '36': 'Fiat',
                    #             '37': 'Honda', '38': 'Isuzu', '39': 'Jaguar',
                    #             '40': 'Lancia', '41': 'Mazda', '42': 'Mercedez Benz',
                    #             '43': 'MG', '44': 'Peugeot', '45': 'Porsche', 
                    #             '46': 'Renault', '47': 'Saab', '48': 'Subaru', 
                    #             '49': 'Toyota', '50': 'Triumph', '51': 'Volvo',
                    #             '52': 'Mitsubishi', '53': 'Suzuki', '54': 'Acura',
                    #             '55': 'Hyundai', '56': 'Merkur', '57': 'Yugo',
                    #             '58': 'Infiniti', '59': 'Lexus', '60': 'Daihatsu', 
                    #             '61': 'Sterling', '62': 'Land Rover', '63': 'KIA',
                    #             '64': 'Daewoo', '65': 'Smart', '66': 'Mahindra', 
                    #             '67': 'Scion', '69': 'Other Import', '70': 'BSA',
                    #             '71': 'Ducati', '72': 'Harley-Davidson', '73': 'Kawasaki', 
                    #             '74': 'Moto-Guzzi', '75': 'Norton', '76': 'Yamaha', 
                    #             '81': 'Reo/Diamond Reo', '82': 'Freightliner', '83': 'FWD', 
                    #             '84': 'Navistar-Intl. Harvest', '85': 'Kenworth', '86': 'Mack', 
                    #             '87': 'Peterbilt', '88': 'Iveco-Magirus', '89': 'White-GMC-Autocar',
                    #             '90': 'Bluebird', '91': 'Eagle Coach', '92': 'Gillig', 
                    #             '93': 'MCI', '94': 'Thomas Built', '98': 'Other', '99': 'Unknown'},
                    # 'MAKE_CD': {1: 'American Motors', 2: 'Jeep-Willys-Kaiser', 3: 'AM General',
                    #             6: 'Chrysler',7: 'Dodge', 8: 'Imperial', 
                    #             9: 'Plymouth', 10: 'Eagle', 12: 'Ford', 
                    #             13: 'Lincoln', 14: 'Mercury', 18: 'Buick/Opel',
                    #             19: 'Cadillac', 20: 'Chevrolet', 21: 'Oldsmobile',
                    #             22: 'Pontiac', 23: 'GMC', 24: 'Saturn', 
                    #             25: 'Grumman', 29: 'Other Domestic', 30: 'Volkswagen', 
                    #             31: 'Alfa Romero', 32: 'Audi', 33: 'Austin/Healey', 
                    #             34: 'BMW', 35: 'Nissan-Datsun', 36: 'Fiat',
                    #             37: 'Honda', 38: 'Isuzu', 39: 'Jaguar',
                    #             40: 'Lancia', 41: 'Mazda', 42: 'Mercedez Benz',
                    #             43: 'MG', 44: 'Peugeot', 45: 'Porsche', 
                    #             46: 'Renault', 47: 'Saab', 48: 'Subaru', 
                    #             49: 'Toyota', 50: 'Triumph', 51: 'Volvo',
                    #             52: 'Mitsubishi', 53: 'Suzuki', 54: 'Acura',
                    #             55: 'Hyundai', 56: 'Merkur', 57: 'Yugo',
                    #             58: 'Infiniti', 59: 'Lexus', 60: 'Daihatsu', 
                    #             61: 'Sterling', 62: 'Land Rover', 63: 'KIA',
                    #             64: 'Daewoo', 65: 'Smart', 66: 'Mahindra', 
                    #             67: 'Scion', 69: 'Other Import', 70: 'BSA',
                    #             71: 'Ducati', 72: 'Harley-Davidson', 73: 'Kawasaki', 
                    #             74: 'Moto-Guzzi', 75: 'Norton', 76: 'Yamaha', 
                    #             81: 'Reo/Diamond Reo', 82: 'Freightliner', 83: 'FWD', 
                    #             84: 'Navistar-Intl. Harvest', 85: 'Kenworth', 86: 'Mack', 
                    #             87: 'Peterbilt', 88: 'Iveco-Magirus', 89: 'White-GMC-Autocar',
                    #             90: 'Bluebird', 91: 'Eagle Coach', 92: 'Gillig', 
                    # #             93: 'MCI', 94: 'Thomas Built', 98: 'Other', 99: 'Unknown'},
                    # 'VEH_TYPE': {1: 'Automobile', 2: 'Motorcycle', 3: 'Bus',
                    #              4: 'Small Truck', 5: 'Large Truck', 6: 'SUV',
                    #              7: 'Van', 10: 'Snowmobile', 11: 'Farm Equipment', 
                    #              12: 'Construction Equipment', 13: 'ATV', 18: 'Other Type-Special Vehicle', 
                    #              19: 'Unknown Type - Special Vehicle', 20: 'Unicycle bicycle or tricycle', 21: 'Other Pedalcycle', 
                    #              22: 'Horse and buggy', 23: 'Horse and rider', 24: 'Train'},
                    'ALCOHOL_RELATED': {0: 'NO', 1: 'YES'}}
    
    rename_vars = ['WEATHER', 'ILLUMINATION', 'ROAD_CONDITION', 'COLLISION_TYPE', 'MAX_SEVERITY_LEVEL', 'INTERSECT_TYPE', 'LOCATION_TYPE', 'ALCOHOL_RELATED']

    for var_name in rename_vars:
        new_col = var_name + '_FULL'
        df[new_col] = df[var_name].map(clean_names[var_name])

    df = df.drop(rename_vars, axis='columns')    
    
    return df


clean_cols = {'MUNICIPALITY': {10212: 'Cranberry Twp', 10101: 'Butler Twp', 10217: 'Jackson Twp', 10301: 'Butler City',
                               10201: 'Adams Twp', 10222: 'Middlesex Twp', 10223: 'Muddy Creek Twp', 10205: 'Center Twp',
                               10204: 'Buffalo Twp', 10228: 'Summit Twp', 10226: 'Penn Twp', 10227: 'Slippery Rock Twp',
                               10211: 'Connoquenessing Twp', 10232: 'Worth Twp', 10219: 'Lancaster Twp', 10422: 'Zelienople Twp',
                               10218: 'Jefferson Twp', 10216: 'Franklin Twp', 10215: 'Forward Twp', 10203: 'Brady Twp',
                               10224: 'Oakland Twp', 10418: 'Slippery Rock Boro', 10207: 'Clay Twp', 10230: 'Washington Twp',
                               10423: 'Seven Fields Boro', 10209: 'Clinton Twp', 10231: 'Winfield Twp', 10214: 'Fairview Twp',
                               10221: 'Mercer Twp', 10206: 'Cherry Twp', 10208: 'Clearfield Twp', 10210: 'Concord Twp',
                               10213: 'Donegal Twp', 10416: 'Prospect Boro', 10415: 'Porttersville Boro', 10413: 'Chicora Boro',
                               10220: 'Marion Twp', 10225: 'Parker Twp', 10410: 'Harrisville Boro', 10404: 'Connoquenessing Boro',
                               10202: 'Allegheny Twp', 10229: 'Venango Twp', 10411: 'Karns City Boro', 10401: 'Bruin Boro',
                               10407: 'Evans City Boro', 10421: 'West Sunbury Boro', 10406: 'Eau Claire Boro', 10403: 'Cherry Valley Boro',
                               10409: 'Harmony Boro', 10414: 'Petrolia Boro', 10402: 'Callery Boro', 10405: 'East Butler Boro',
                               10408: 'Fairview Boro', 10412: 'Mars Boro', 10417: 'Saxonburg Boro', 10419: 'Valencia Boro',
                               10420: 'West Liberty Boro'}}
            #    'WEATHER_FULL': {'Fog': 'Other', 'Sleet or Hail': 'Other', 'Unknown': 'Other', 'Rain and Fog': 'Other', 'Sleet and Fog': 'Other'}}

renames = ['MUNICIPALITY']

def clean_df(df, names, rename_vars):

    for var_name in rename_vars:
        new_col = var_name + '_FULL'
        df[new_col] = df[var_name].map(names[var_name])

    df = df.drop(rename_vars, axis='columns')    
    
    return df