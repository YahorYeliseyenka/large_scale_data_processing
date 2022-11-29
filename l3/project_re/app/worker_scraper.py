import datetime as dt

from celery_base import app, FETCHING_INTERVAL, SUBREDDIT_NAMES, SUBMISSION_NUM, REDDIT
from docker_logs import get_logger
from scraper import get_new_submission_urls, get_submission_data


logging = get_logger("worker-scraper")
logging.propagate = False


@app.task(name='scrap_submission', serializer='pickle')
def scrap_submission(submission_url):
    submission = get_submission_data(REDDIT, submission_url)    
    app.send_task('calculate_embedding', queue='embedding', kwargs={'submission':submission})


@app.task(name='scrap_subreddits', serializer='pickle')
def scrap_subreddits():
    last_scrap_time = dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=FETCHING_INTERVAL)
    for s_name in SUBREDDIT_NAMES:
        new_submission_urls = get_new_submission_urls(REDDIT, s_name, SUBMISSION_NUM, last_scrap_time)

        logging.info(f'Processing {len(new_submission_urls)} submissions from {s_name} subreddit added after {last_scrap_time}.')

        for submission_url in new_submission_urls:
            scrap_submission.delay(submission_url)

        logging.info(f'Processed ---> {s_name} <--- subreddit.')