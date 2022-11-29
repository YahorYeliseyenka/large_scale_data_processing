# https://www.storybench.org/how-to-scrape-reddit-with-python/
import praw
import datetime as dt
import pandas as pd

from os import path


def get_credentials(bot='bot1'):
    return praw.Reddit(bot)


def get_submittion_data(reddit, url):
    submission = reddit.submission(url)
    return {
        "id":submission.id, 
        "url":submission.url, 
        "title":submission.title, 
        "body":submission.selftext,  
        "created":get_date(submission.created),
        "author":submission.author,
        "score":submission.score,
        "upvote_ratio":submission.upvote_ratio,
        "crossposts_num":submission.num_crossposts,
        "over_18":submission.over_18,
        "comms_num":submission.num_comments
    }


def get_topics_data(reddit, subreddit_name, topic_num):
    subreddit = reddit.subreddit(subreddit_name)
    new_subreddit = subreddit.new(limit=topic_num)
    topics_dict = { "id":[], 
                    "url":[], 
                    "title":[], 
                    "body":[],  
                    "created":[],
                    "author":[],
                    "score":[],
                    "upvote_ratio":[],
                    "crossposts_num":[],
                    "over_18":[],
                    "comms_num":[]
                    }

    for submission in new_subreddit:
        topics_dict["id"].append(submission.id)
        topics_dict["url"].append(submission.url)
        topics_dict["title"].append(submission.title)
        topics_dict["body"].append(submission.selftext)
        topics_dict["created"].append(get_date(submission.created))
        topics_dict["author"].append(submission.author)
        topics_dict["score"].append(submission.score)
        topics_dict["upvote_ratio"].append(submission.upvote_ratio)
        topics_dict["crossposts_num"].append(submission.num_crossposts)
        topics_dict["over_18"].append(submission.over_18)
        topics_dict["comms_num"].append(submission.num_comments)    

    topics_df = pd.DataFrame(topics_dict)
    
    return topics_df


def get_date(created):
    return dt.datetime.fromtimestamp(created) - dt.timedelta(hours=8)