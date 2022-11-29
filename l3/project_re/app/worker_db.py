# https://www.bogotobogo.com/python/MongoDB_PyMongo/python_MongoDB_pyMongo_tutorial_connecting_accessing.php

import pymongo
import pandas as pd

from celery_base import app
from docker_logs import get_logger
from dataclasses import asdict
from pymongo import MongoClient
from dataclasses import asdict


logging = get_logger("worker-db")
logging.propagate = False

# def save_csv(submission, filename='temp.csv'):
#     df = pd.DataFrame.from_records([asdict(submission)])
#     df.to_csv(filename, sep=';', header=True, decimal=',', mode='w',
#                 doublequote=True)


@app.task(name='save2db', serializer='pickle', queue='db_worker')
def save2db(submission):
    client = MongoClient('mongodb://admin:admin@database:27017/')
    mydb = client['dbsubmissions']
    result = mydb.submission.insert_one(asdict(submission))
    # logging.info(f'ID: {result.inserted_id} added to DB')