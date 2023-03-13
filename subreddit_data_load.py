import glob
import pandas as pd

import pathlib
import os
# For list of subreddits, make each subreddit name a path object we can paste into overall path
subreddit_list = ['suboxone', 'methadone', 'opiates', 'OpiateRecovery']

#rootdir = os.path.join(r'INSERT SUBREDDIT FILE DIRECTORY HERE')
data = []
for subreddit in subreddit_list:
    rootdir = os.path.join(r'C:\Users\awalk55\OneDrive - Emory University\Desktop\stigma_and_bias_suboxone_methadone\newsubs', subreddit)
    rootdir = pathlib.Path(rootdir)
        for file in rootdir.glob('*.tsv'):
            print(file)
            df = pd.read_csv(file, sep='\t')
            data.append(df)
            bigdf = pd.concat(data)

bigdf.to_csv("all_subreddit_posts.csv")

