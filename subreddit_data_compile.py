import glob
import pandas as pd
import difflib

import pathlib
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
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
bigdf_sample = bigdf['body'].sample(n = 1000)


words = bigdf_sample.to_string().split()
def matches(large_string, query_string, threshold):
    words = large_string.split()
    for word in words:
        s = difflib.SequenceMatcher(None, word, query_string)
        match = ''.join(word[i:i+n] for i, j, n in s.get_matching_blocks() if n)
        if len(match) / float(len(query_string)) >= threshold:
            yield match

stigma_words = " ".join(["abuser","junkie","alcoholic","drunk","habit","dirty","stigma","bias","stereotype","shame","blame"])
words_string = " ".join(words)
match_list = list(matches(words_string, "shame", 0.9))

# Next step: use bias lexicon to search for any posts with mentions of lexicon words
# How to incorporate a Levenstein ratio match to "fuzzy join" these words

bias_big_df = bigdf[bigdf['body'].str.contains('abuser|junkie|alcoholic|drunk|habit|dirty|stigma|bias|stereotype|shame|blame|user', na=False)]

# Validation?
bias_big_df.to_csv("all_subreddit_bias_posts.csv")
# Visualizations-- plotting frequencies over time, prevalences within each of the communities
# https://www.datacamp.com/community/tutorials/fuzzy-string-python

# for loop that goes through
# for post in subreddit posts
# if word in post is <= .9 Lev distance of any words in stigmawords
# then append dataframe