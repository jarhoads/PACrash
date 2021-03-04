import pandas as pd

def merge_dfs(file_list):

    dfs = []
    for f in file_list:
        df = pd.read_csv(f, engine='python')
        cols = list(df)
        df[cols] = df[cols].astype(str)

        dfs.append(df)

    # dfs = [pd.read_csv(file_name, engine='python') for file_name in file_list]
    return dfs[0].append(dfs[1:])