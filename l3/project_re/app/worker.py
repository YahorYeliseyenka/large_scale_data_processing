from celery_base import app, FETCHING_INTERVAL, SUBMISSION_NUM
from docker_logs import get_logger
from worker_scraper import scrap_subreddits


logging = get_logger("worker")
logging.propagate = False

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(FETCHING_INTERVAL, scrap_subreddits.s())