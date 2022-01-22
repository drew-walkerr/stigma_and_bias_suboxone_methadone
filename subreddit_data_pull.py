import praw, prawcore
import re, string
import pandas as pd
import os
import scipy
import nltk
#read in client_id, secret, user_agent to access the API through subreddit_data_api.csv file
api = pd.read_csv("subreddit_data_api.csv",header=None)
#remove header
api.iloc[0,0]
api.iloc[1,0]
api.iloc[2,0]

def connectToReddit():
    reddit = praw.Reddit(client_id=api.iloc[0,0],
                     client_secret=api.iloc[1,0],
                     user_agent=api.iloc[2,0])
    return reddit



#Search suboxone posts for ones containing bias words "OR stereotype OR abuser OR discrimin OR judge"

# Below functions are Dr. Sarker's code to pull data from multiple subreddits


def collectAllDataFromSubreddit(reddit,subreddit_list):
    '''
    given a set of subreddit names, collects all data from the subreddits...
    :param subreddit_list:
    :return:
    '''
    #subreddit_list = []

    #infile = open('./subreddit_names')
    #infile = open('./nida_subs')
    #already_collected = os.listdir('/Volumes/N1Mac/subreddit_data/')
    #for line in infile:
    #    subreddit_list.append(str.strip(line))
    print('Number of subreddits',len(subreddit_list))
    for subreddit_name in subreddit_list:
      #if not subreddit_name in already_collected:
        try:
            if not os.path.exists('./newsubs/' + subreddit_name):
                os.makedirs('./newsubs/' + subreddit_name)
            #if not os.path.exists('/Volumes/N1Mac/subreddit_data/'+subreddit_name):
            #    os.mkdir('/Volumes/N1Mac/subreddit_data/'+subreddit_name)
            subreddit = reddit.subreddit(subreddit_name)
            print(subreddit)

            count = 0

            top_subreddit = subreddit.top(limit=None)
            for submission in top_subreddit:
                table = []
                print('collecting', submission.id, subreddit_name)
                try:
                    table.append([submission.id, str(submission.author), int(submission.created_utc), str('True'), 'NA',
                                  str(submission.permalink), str(submission.score), str(submission.subreddit_id),
                                  str(submission.selftext.encode('utf-8', 'ignore'))])
                    submission.comments.replace_more(limit=None)
                    comments = submission.comments.list()
                    for comment in comments:
                        count += 1

                        id_ = comment.id
                        author = comment.author
                        created = comment.created_utc
                        is_submitter = comment.is_submitter
                        # link_id = comment.link_id
                        parent_comment = comment.parent_id
                        permalink = comment.permalink
                        score = comment.score
                        subreddit_id = comment.subreddit_id
                        body = comment.body
                        row = [id_, str(author), int(created), is_submitter, parent_comment, permalink, score, subreddit_id, body]
                        table.append(row)
                    subreddit_df = pd.DataFrame(table,
                                                columns=['id_', 'author', 'created', 'is_submitter', 'paren_comment_id', 'permalink',
                                                         'score', 'subreddit_id', 'body'])
                    subreddit_df['created'] = pd.to_datetime(subreddit_df['created'], unit='s')
                    print(len(subreddit_df))
                    out = re.sub(r'[^\w\s]', '', submission.title[:250])
                    subreddit_df.to_csv('./newsubs/' + subreddit_name + '/' + out + '.tsv', sep='\t', encoding='utf-8')
                except:
                    print('there was an error with submission', submission.id,subreddit_name)
        except prawcore.exceptions.NotFound:
            print ('Subreddit not available',subreddit_name)
        except prawcore.exceptions.Forbidden:
            print('Subreddit forbidden',subreddit_name)
        except prawcore.exceptions.Redirect:
            print('Subreddit redirected...')

def getCommentsByUser(reddit,redditor_name):
    all_comments_obtained = False
    all_submissions_obtained = False
    #first, obtain existing posts by the user that have been collected
    #collected_comments = pd.read_csv('/Volumes/CommonDF/RedditData/users2/' + redditor_name + '.tsv', sep='\t', encoding='utf-8')
    #comment_ids = list(collected_comments['id_'])
    #collected_comments.created = pd.to_datetime(collected_comments.created,utc=True)
    #print(collected_comments.created[1])
    #print(collected_comments['created'][1])
    #print(collected_comments.dtypes)
    user = reddit.redditor(redditor_name)
    #for comment in user.get_comments(limit=None):
    #    print comment.body
    comment_ids = []
    redditor_name = redditor_name
    table = []
    for comment in user.comments.new(limit=None):

        #try:
            #print comment
            comment_id = comment.id
            if not comment_id in comment_ids:
                comment_text =  comment.body
                #print comment_text
                comment_submission_title = comment.submission.title
                #print comment_submission_title
                #print comment.submission.author
                comment_submission_author = comment.submission.author

                created = comment.created_utc
                #print(created)
                comment_id = comment.id
                comment_subreddit = comment.subreddit.display_name
                comment_ids.append(comment_id)
                #to_append = [None,comment_id,created,comment_submission_author,comment_submission_title,comment_text,comment_subreddit]
                #collected_comments.append(pd.Series(to_append, index=collected_comments.columns),ignore_index=True)
                #print comment_id,'\t',created,'\t',comment_submission_author_id,'\t',comment_submission_title,'\t',comment_text
                table.append([comment_id,created,comment_submission_author,comment_submission_title,comment_text,comment_subreddit])
            else:
                all_comments_obtained = True
                break
            #except:
            #    print 'exception'

    for submission in user.submissions.new(limit=None):
        #try:

        submission_id = submission.id
        if not submission_id in comment_ids:
            submission_title = submission.title
            submission_text = submission.selftext
            created =submission.created_utc

            submission_author = submission.author
            submission_subreddit = submission.subreddit.display_name
            comment_ids.append(submission_id)
            #to_append = [None,comment_id, created, comment_submission_author, comment_submission_title, comment_text,
            #             comment_subreddit]
            #collected_comments.append(pd.Series(to_append, index=collected_comments.columns),ignore_index=True)
            table.append([submission_id,created,submission_author,submission_title,submission_text,submission_subreddit])
        else:
            all_submissions_obtained = True

            break
            #print submission_id,'\t',created,'\t',submission_author_id,'\t',submission_title,'\t',submission_text
        #except:
        #    print 'exception'
    user_profile_df = pd.DataFrame(table,
                                   columns=['id_', 'created', 'submission_author_id',
                                            'submission_title', 'submission_text','submission_subreddit'])
    if all_comments_obtained == False or all_comments_obtained == False:
        outfile = open('./to_collect/'+redditor_name,'w')
        outfile.write(str(redditor_name)+'\t'+str(all_comments_obtained)+'\t'+str(all_submissions_obtained))
        outfile.close()
    #user_profile_df = collected_comments
    user_profile_df = user_profile_df.sort_values(['created'])
    user_profile_df['created'] = pd.to_datetime(user_profile_df['created'], unit='s')
    #user_profile_df.to_csv('/Volumes/CommonDF/RedditData/users_dec2021/' + redditor_name + '.tsv', sep='\t', encoding='utf-8')
    user_profile_df.to_csv('./new_users/'+redditor_name+'.tsv',sep='\t', encoding='utf-8')
if __name__=='__main__':
    reddit = connectToReddit()
    print(reddit.user.me())
    subreddit_list = ['suboxone','methadone','opiates','OpiateRecovery']


    collectAllDataFromSubreddit(reddit,subreddit_list)


    count = 0



