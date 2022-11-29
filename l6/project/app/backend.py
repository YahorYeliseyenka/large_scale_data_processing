import shutil
import pyspark
import numpy as np
import uvicorn
import pandas as pd
from fastapi import FastAPI
from pymagnitude import Magnitude
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.sql.functions import udf


app = FastAPI()
FASTTEXT = Magnitude("word2vec.magnitude")

# spark = pyspark.sql.SparkSession.builder.appName("myApp").getOrCreate()
spark = SparkSession.builder.appName("myApp").getOrCreate()
model_unpacked = "./model_path"
# shutil.unpack_archive("my_model.zip", model_unpacked)
trainedModel = PipelineModel.load(model_unpacked)


def get_pred(title, subreddit):
    df = spark.createDataFrame([(title, subreddit)], ["title", "subreddit"])
    to_vector = udf(lambda a: Vectors.dense(a), VectorUDT())
    data = df.select(to_vector("title").alias("text_embedding"), "subreddit")

    predictions = trainedModel.transform(data).collect()
    preds = [x['prediction'] for x in predictions]
    return preds[0]


def get_embedding(text):
    words_embedding = FASTTEXT.query(text.split())
    embedding = np.mean(words_embedding, axis=0)
    return embedding.tolist()


@app.get("/")
def read_root():
    return "Welcome!"


@app.post("/{title}/{subreddit}")
def parse(title: str, subreddit: str):
    res = get_pred(get_embedding(title), subreddit)
    return {"res": res}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
    # app.run()