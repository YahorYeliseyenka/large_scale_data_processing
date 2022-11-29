# https://www.storybench.org/how-to-scrape-reddit-with-python/
import praw
import datetime as dt

from os import path
from submission import Submission


def get_credentials(bot='bot1'):
    return praw.Reddit(bot)


def get_new_submission_urls(reddit, subreddit_name, submissions_num, last_scrap_time):
    subreddit = reddit.subreddit(subreddit_name)
    submissions = subreddit.new(limit=submissions_num)
    
    new_submission_urls = []
    for submission in submissions:
        if get_date(submission.created) > last_scrap_time:
            new_submission_urls.append(submission.shortlink)
    
    return new_submission_urls


def get_submission_data(reddit, submission_url):
    topic = reddit.submission(url=submission_url)
    return Submission(  topic.shortlink, 
                        topic.author.name, 
                        topic.subreddit.display_name, 
                        topic.selftext, 
                        None, 
                        topic.upvote_ratio, 
                        topic.score,
                        topic.over_18, 
                        topic.num_comments, 
                        topic.title, 
                        get_date(topic.created)
                    )
    

def get_date(created):
    return dt.datetime.fromtimestamp(created, dt.timezone.utc) - dt.timedelta(hours=8)