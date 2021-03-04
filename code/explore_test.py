import explore
import chisquare
import pandas as pd
import seaborn as sns
import numpy as np

cs_vars = []


def main():

    print("opening crash dataframe")
    crash_df = explore.read_crash_data()
    print("crash dataframe opened")

    print("-- displaying missing values")
    missing = crash_df.isnull().sum()
    print("Missing Values: {0}".format(missing))

    crash_vars = explore.keep_vars()

    print("-- performing chi-squared analysis")
    crash_cs_vars = crash_vars['categorical'] + ['ALCOHOL_RELATED_FULL']
    crash_df_chisq = crash_df[crash_cs_vars]
    cs_test = chisquare.ChiSquare(crash_df_chisq)

    for var in crash_cs_vars[:-1]:
        cs_test.test_independence(colX=var, colY="ALCOHOL_RELATED_FULL")
    
    print(cs_test.important_vars)
    print(cs_test.non_important_vars)

    cs_vars.append(cs_test.important_vars)

    # # clean the ROUTE variable
    # clean_replace = {'SPEED_LIMIT': 0, 'STREET_NAME':'UNKNOWN', 'SEGMENT':'UNKNOWN', 'OFFSET':'UNKNOWN','SCH_BUS_IND': 'N', 'SCH_ZONE_IND': 'N', 'ACCESS_CTRL': 'UNKNOWN'}
    # crash_df_clean = crash_df.fillna(clean_replace)
    # crash_df_clean.ROUTE = crash_df_clean.ROUTE.fillna(value=crash_df_clean.STREET_NAME)
    # # crash_df_clean = explore.clean_route(crash_df)
    # print(crash_df_clean.head())
    # missing_clean = crash_df_clean.isnull().sum()
    # print("Missing Values: {0}".format(missing_clean))

    # correlation chart
    # cv_numerics = crash_vars['people'] + crash_vars['auto'] + crash_vars['other_numeric']
    # cv_numerics = crash_vars['numeric']
    # cv_num_df = crash_df[cv_numerics]
    # explore.corr_chart(cv_num_df)

    # heatmap
    df_hm_vars = crash_vars['date_time'] + ['CRN']
    df_hm = crash_df[df_hm_vars]
    explore.heatmap_chart(df_hm)
    # df_hm_pivot = pd.pivot_table(df_hm, values='CRASH_CRN', index=['CRASH_MONTH'], columns=['DAY_OF_WEEK'], aggfunc=np.count_nonzero)
    # ax = sns.heatmap(df_hm_pivot)
    # plt.show()

    # print(cs_vals)

main()


# grouped_ehc_hour = crash_df['EST_HRS_CLOSED'].groupby(crash_df['HOUR_OF_DAY'])
# grouped_ehc_hour.sum()
# grouped_auto_hour = crash_df['AUTOMOBILE_COUNT'].groupby(crash_df['HOUR_OF_DAY'])
# grouped_auto_hour.sum()
# plt.scatter(grouped_ehc_hour.sum(), grouped_auto_hour.sum())