#ERROR IN PYSPARK SCRIPT
#IT CAN NOT INFER THE DATABASE CREATED BY GLUE

"""import boto3
from pyspark import SparkConf, SparkContext, SQLContext

s3 = boto3.client("s3")
jsonFile = s3.get_object(Bucket="aws-training-umartahir-glue-data",Key="raw/2015-01-01-15.json")
s3_clientdata = jsonFile['Body'].read().decode('utf-8')

conf = SparkConf()
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

path = "s3a://aws-training-umartahir-glue-data/processed-data/"
rdd = sc.parallelize(s3_clientdata)

rdd.toDF(["id","type","CreateEvent","actor"]).write.parquet(path)
"""

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource0 = glueContext.create_dynamic_frame.from_catalog(database = "git-db", table_name = "raw", transformation_ctx = "datasource0")
applymapping1 = ApplyMapping.apply(frame = datasource0, mappings = [("id", "string", "id", "string"), ("type", "string", "type", "string"), ("payload", "struct", "payload", "struct"), ("repo", "struct", "repo", "string"), ("actor", "struct", "actor", "string")], transformation_ctx = "applymapping1")
resolvechoice2 = ResolveChoice.apply(frame = applymapping1, choice = "make_struct", transformation_ctx = "resolvechoice2")
dropnullfields3 = DropNullFields.apply(frame = resolvechoice2, transformation_ctx = "dropnullfields3")
datasink4 = glueContext.write_dynamic_frame.from_options(frame = dropnullfields3, connection_type = "s3", connection_options = {"path": "s3://aws-training-umartahir-glue-data/processed"}, format = "parquet", transformation_ctx = "datasink4")

job.commit()




