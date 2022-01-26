import glob
import pandas as pd

import pathlib
import os

subreddit_list = ['suboxone', 'methadone', 'opiates', 'OpiateRecovery']
path_list = []
for subreddit in subreddit_list:
    path = pathlib.Path(subreddit)
    path_list.append(path)

#rootdir = pathlib.Path(r'C:\Users\awalk55\PycharmProjects\stigma_and_bias_suboxone_methadone\newsubs\methadone')
data = []
for subreddit in path_list:
    rootdir = os.path.join(r'C:\Users\awalk55\PycharmProjects\stigma_and_bias_suboxone_methadone\newsubs', subreddit)
    rootdir = pathlib.Path(rootdir)
        for file in rootdir.glob('*.tsv'):
         print(file)
         df = pd.read_csv(file, sep='\t')
         data.append(df)
bigdf = pd.concat(data)  # or pd.concat(data, axis='columns')
# need to investigate nested for loops to make sure this iterates over each set of folders 
