import numpy as np

from celery_base import app
from docker_logs import get_logger
from worker_db import save2db
from pymagnitude import Magnitude


logging = get_logger("worker_embedding")
logging.propagate = False

@app.task(name='calculate_embedding', serializer='pickle', queue='embedding')
def calculate_embedding(submission):
    FASTTEXT = Magnitude("glove.magnitude")
    
    text = submission.title
    words_embedding = FASTTEXT.query(text.split())
    embedding = np.mean(words_embedding, axis=0)
    submission.text_embedding = embedding.tolist()
    save2db.s(submission).apply_async(queue='db_worker')