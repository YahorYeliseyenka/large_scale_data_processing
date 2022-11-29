# https://docs.celeryproject.org/en/stable/userguide/routing.html#defining-queues
from celery import Celery
from docker_logs import get_logger
from kombu import Exchange, Queue
from scraper import get_credentials


logging = get_logger("task")
logging.propagate = False

FETCHING_INTERVAL = 60*5
SUBREDDIT_NAMES = ['announcements', 'funny', 'AskReddit', 'gaming', 'aww', 'science']
SUBMISSION_NUM = 100
REDDIT = get_credentials()


app = Celery()

app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['pickle']

default_exchange = Exchange('default', type='direct')
embedding_exchange = Exchange('embedding', type='direct')
db_worker_exchange = Exchange('db_worker', type='direct')

app.conf.task_queues = (
    Queue('default', default_exchange, routing_key='default'),
    Queue('embedding', embedding_exchange, routing_key='embedding'),
    Queue('db_worker', db_worker_exchange, routing_key='db_worker')
)
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange = 'default'
app.conf.task_default_routing_key = 'default'
