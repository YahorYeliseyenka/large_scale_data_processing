from celery_base import app, get_new_topics
from random import random
from docker_logs import get_logger

# logging_child = get_logger("child")
# logging_child.propagate = False
logging = get_logger("runner")
# logging.propagate = False

FATCHING_INTERVAL = 60*10
SUBREDDIT_NAME = 'All'
TOPIC_NUM = 100

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(FATCHING_INTERVAL, get_new_topics.s(FATCHING_INTERVAL, SUBREDDIT_NAME, TOPIC_NUM))