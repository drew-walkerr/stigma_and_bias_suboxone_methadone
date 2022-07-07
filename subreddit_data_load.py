import glob
import pandas as pd

import pathlib
import os
# For list of subreddits, make each subreddit name a path object we can paste into overall path
subreddit_list = ['suboxone', 'methadone', 'opiates', 'OpiateRecovery']
path_list = []
for subreddit in subreddit_list:
    path = pathlib.Path(subreddit)
    path_list.append(path)

#rootdir = os.path.join(r'INSERT SUBREDDIT FILE DIRECTORY HERE')
data = []
for subreddit in path_list:
    rootdir = os.path.join(r'C:\Users\awalk55\PycharmProjects\stigma_and_bias_suboxone_methadone\newsubs', subreddit)
    rootdir = pathlib.Path(rootdir)
        for file in rootdir.glob('*.tsv'):
         print(file)
         df = pd.read_csv(file, sep='\t')
         data.append(df)
    bigdf = pd.concat(data)

bigdf.to_csv("all_subreddit_posts.csv")

# Next step: use bias lexicon to search for any posts with mentions of lexicon words
# Read in bias words, separate by |
bias_words = pd.read_csv("word_list_expanded.csv")
word_list = bias_words["stem_word"]
#Testing search on dataframe
bias_big_df = bigdf[bigdf['body'].str.contains('abuser|junkie|alcoholic|drunk|habit|dirty|stigma|bias|stereotype|shame|blame', na=False)]

