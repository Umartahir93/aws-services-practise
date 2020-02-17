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

#read file from s3
readPath="s3://aws-umartahir-glue-data/data.csv"
df= spark.read.csv(readPath, mode="DROPMALFORMED",inferSchema=True, header = True)

#write file to s3 in parquet mode
writePath="s3://aws-umartahir-glue-data/transform-data.csv"
df.write.parquet(writePath)


#read parquet mode
df= spark.read.parquet(writePath)
df.show(5)

job.commit()
