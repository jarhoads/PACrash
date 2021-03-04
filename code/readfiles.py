'''
CSV Quoted Data Module for Pennsylvania Crash Data
Joshua Rhoads 2019
'''

import csv


def read_quoted(filename):
    '''
    read in a comma delimited file with values as strings
    convert each record to a python list
    write the lines back out as a simple csv file without strings
    '''

    lines = []
    print('Opening {0}'.format(filename))
    with open(filename, 'r') as f:
        lines = list(csv.reader(f))

    # find the location of '.csv' in the file
    # and add _edit to the end
    csv_str = '.csv'
    csv_loc = filename.find(csv_str)
    outfile_name = filename[:csv_loc] + '_E.csv'
    print('output file will have name: {0}'.format(outfile_name))

    with open(outfile_name, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(lines)
    
    f.close()
    outfile.close()
