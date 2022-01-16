import praw
import pandas as pd
import nltk
#read in client_id, secret, user_agent to access the API through subreddit_data_api.csv file
api = pd.read_csv("subreddit_data_api.csv",header=None)
#remove header
api.iloc[0,0]
api.iloc[1,0]
api.iloc[2,0]
#use praw to access reddit api
reddit = praw.Reddit(client_id=api.iloc[0,0],
                     client_secret=api.iloc[1,0],
                     user_agent=api.iloc[2,0])




#Search suboxone posts for ones containing bias words "OR stereotype OR abuser OR discrimin OR judge"
posts = []
suboxone_posts = reddit.subreddit('Suboxone').search("stigma OR bias OR stereotype OR abuser OR discrimin")
for post in suboxone_posts:
    posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created,post.comments])
print(posts)

for submission in suboxone_posts:
    print(suboxone_posts.title)
    suboxone_posts.comments.replace_more(limit=None)
    for comment in suboxone_posts.comments.list():
        print(comment.author)
        print(comment.score)
        print(comment.created_utc)  # as a Unix timestamp
        print(comment.body)

