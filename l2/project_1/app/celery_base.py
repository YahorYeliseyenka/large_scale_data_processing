import datetime as dt

from celery import Celery
from docker_logs import get_logger
from scraper import get_credentials, get_submittion_data, get_topics_data
from prometheus_client import Histogram, Counter
from numpy import arange


# logging_child = get_logger("child")
# logging_child.propagate = False
logging = get_logger("task")
# logging.propagate = False

app = Celery()

reddit = get_credentials()
submissions_counter = Counter('submissions_counter', 'Submissions counter')
bodys_counter = Counter('bodys_counter', 'Body counter')
publications_hours = Histogram('publications_hours', 'Histogram of submissions publications hours', buckets=range(0, 24))
titles_length = Histogram('titles_length', 'Histogram of topics length', buckets=range(0, 500, 50))
fetching_time = Histogram('fetching_time', 'Submissions fetch time', buckets=arange(0, 10, 0.5))


@app.task(name='get_submittion_data')  
def get_submittion(url):  
    submission_dict = get_submittion_data(reddit, url)
    logging.info(f'Processed submittion TITLE: {submission_dict["title"]}, DATA_INS: {submission_dict["created"]}')


@app.task(name='get_topics_data')  
def get_new_topics(fatching_interval, subreddit_name, topic_num):
    start = dt.datetime.now()
    topic_df = get_topics_data(reddit, subreddit_name, topic_num)
    finish = dt.datetime.now()

    fetching_time.observe((finish - start).total_seconds())

    topic_df = topic_df[topic_df.created >= start - dt.timedelta(seconds=fatching_interval)]
    new_topics_num = topic_df.shape[0]

    logging.info(f"Fetched {new_topics_num} new submissions.")

    submissions_counter.inc(topic_df.shape[0])
    bodys_counter.inc((topic_df['body'].values != '').sum())
    for index, topic in topic_df.iterrows():
        titles_length.observe(len(topic.title))
        publications_hours.observe(topic.created.hour)