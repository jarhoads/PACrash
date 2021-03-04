from scipy import stats
import numpy as np

def fix_skew(df_col):
    # get values from column
    col_values = np.asarray(df_col.values)

    # transform values using boxcox transform
    transform = stats.boxcox(col_values)[0]

    return transform
