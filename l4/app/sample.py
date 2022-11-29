"""Sample pySpark app."""
# https://towardsdatascience.com/building-a-linear-regression-with-pyspark-and-mllib-d065c3ba246a
# https://stackoverflow.com/questions/42138482/how-do-i-convert-an-array-i-e-list-column-to-vector
# https://datascience.stackexchange.com/questions/57481/how-to-deal-with-evaluations-in-a-multi-step-ml-pipeline
# import mleap.pyspark
# from mleap.pyspark.spark_support import SimpleSparkSerializer
import shutil

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexer, Binarizer, Tokenizer, HashingTF, CountVectorizer, StopWordsRemover
from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.sql.functions import udf
from pyspark.ml.regression import LinearRegression
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import RegressionEvaluator, MulticlassClassificationEvaluator


conf = SparkConf().setAppName('myApp').setMaster('local')\
    .set("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.3.4")
sc = SparkContext(conf=conf)
sc.setLogLevel("OFF")

mongo_uri = "mongodb://admin:admin@mongodb:27017/dbsubmissions.submission"

col_names = ["subreddit_num", "comments_num", "over_18", "score", "upvote_ratio", "text_embedding"]


def getStages(col_name):
    stage1 = StringIndexer(inputCol="subreddit", outputCol="subreddit_num")
    
    inputCols = [col for col in col_names if col is not col_name]
    stage3 = VectorAssembler(inputCols=inputCols,
                            outputCol="features")
    return [stage1, stage3]


def getStagesL6():
    label_stringIdx = StringIndexer(inputCol="subreddit", outputCol="label")
    
    # tokenizer = Tokenizer(inputCol="title", outputCol="words")
    # add_stopwords = ["http","https","amp","rt","t","c","the"] 
    # stopwordsRemover = StopWordsRemover(inputCol="words", outputCol="filtered").setStopWords(add_stopwords)
    # countVectors = CountVectorizer(inputCol="filtered", outputCol="title_vec", vocabSize=10000, minDF=5)

    inputCols = ["text_embedding", "label"]
    final_stage = VectorAssembler(inputCols=inputCols, outputCol="features")

    return [label_stringIdx, final_stage]


def trainModelL6(train, test, labelCol):
    stages = getStagesL6()
    model = LogisticRegression(featuresCol = 'features', labelCol=labelCol, maxIter=10, regParam=0.3, \
                            elasticNetParam=0.8, family="multinomial")
    stages.append(model)

    evaluator = MulticlassClassificationEvaluator(predictionCol="prediction",
                                                  labelCol=labelCol,
                                                  metricName='f1')

    pipeline = Pipeline(stages=stages)
    model = pipeline.fit(train)
    train_preds = model.transform(train)
    test_preds = model.transform(test)
    return evaluator.evaluate(train_preds), evaluator.evaluate(test_preds), model, test_preds


def trainModel(train, test, col_name):
    stages = getStages(col_name)
    model = None
    evaluator = None

    if col_name is 'upvote_ratio':
        model = LinearRegression(featuresCol = 'features', labelCol=col_name, maxIter=10, regParam=0.3, \
                            elasticNetParam=0.8)
        evaluator = RegressionEvaluator(predictionCol="prediction",
                                    labelCol=col_name,
                                    metricName='rmse')
    elif col_name is 'over_18':
        model = LogisticRegression(featuresCol = 'features', labelCol=col_name, maxIter=10, regParam=0.3, \
                            elasticNetParam=0.8, family="multinomial")
        evaluator = MulticlassClassificationEvaluator(predictionCol="prediction",
                                                  labelCol=col_name,
                                                  metricName='f1')
    else:
        model = LogisticRegression(featuresCol = 'features', labelCol=col_name, maxIter=10, regParam=0.3, \
                            elasticNetParam=0.8)
        evaluator = MulticlassClassificationEvaluator(predictionCol="prediction",
                                                  labelCol=col_name,
                                                  metricName='f1')

    stages.append(model)
    pipeline = Pipeline(stages=stages)
    fit_pipeline = pipeline.fit(train)
    train_preds = fit_pipeline.transform(train)
    test_preds = fit_pipeline.transform(test)
    return evaluator.evaluate(train_preds), evaluator.evaluate(test_preds)


my_spark = SparkSession \
    .builder \
    .appName("myApp") \
    .config("spark.mongodb.input.uri", mongo_uri) \
    .getOrCreate()

df = my_spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
# -----------------------------------------------------------------------------------
list_to_vector_udf = udf(lambda l: Vectors.dense(l), VectorUDT())
df = df.withColumn("text_embedding",list_to_vector_udf(df["text_embedding"]).alias("text_embedding"))
df = df.withColumn("over_18",df["over_18"].cast("int"))

indexers = [StringIndexer(inputCol=column, outputCol=column+"_index").fit(df) for column in list(set(["subreddit"]))]

pipeline = Pipeline(stages=indexers)
df_r = pipeline.fit(df).transform(df)

for i in range(20):
    print(df_r.filter(df_r.subreddit_index == i*1.0).select("subreddit", "subreddit_index").first())
# -----------------------------------------------------------------------------------
# list_to_vector_udf = udf(lambda l: Vectors.dense(l), VectorUDT())

# df = df.withColumn("text_embedding",list_to_vector_udf(df["text_embedding"]).alias("text_embedding"))
# df = df.withColumn("over_18",df["over_18"].cast("int"))

# print(f"Dataframe spape: {df.count()}: {len(df.columns)}")

# train, test = df.randomSplit([0.7, 0.3], seed=12)

# trainRes, testRes, model, pred = trainModelL6(train, test, "over_18")
# print(f"Multi-class Classification F-Measure Train = {trainRes} / {testRes}")

# model.write().overwrite().save("model_path")
# path_drv = shutil.make_archive("my_model", format='zip', base_dir="model_path")

# -----------------------------------------------------------------------------------
# model.serializeToBundle("jar:file:/tmp/model.zip", pred.limit(0))


# train_rmse, test_rmse = trainModel(train, test, "upvote_ratio")
# print(f"Regression RMSE Train / Test = {train_rmse} / {test_rmse}")

# train_f1, test_f1 = trainModel(train, test, "over_18")
# print(f"Binary Classification F-Measure Train / Test = {train_f1} / {test_f1}")

# train_f1, test_f1 = trainModel(train, test, "subreddit_num")
# print(f"Multi-class Classification F-Measure Train / Test = {train_f1} / {test_f1}")