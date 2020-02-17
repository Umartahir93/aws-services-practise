import boto3, botocore
import time
import datetime

#FINAL CONSTANTS VARIABLES
bucket_name = 'awstraining.umartahir.consumerbucket'
s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
my_stream_name = 'aws-training-umartahir'


#UTILITY FUNCTIONS STARTS HERE
def get_filename_datetime():
    x = datetime.datetime.now()
    return "file-" + str(x) + ".txt"


def create_File(name,record_response):
    path = name
    with open(path, "w") as f:
        f.write(str(record_response))
        print(str(record_response))
        f.close()

    return path

def check_bucket(bucket):
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
        print("Bucket Exists!")
        return True

    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 403:
            print("Private Bucket. Forbidden Access!")
            return True
        elif error_code == 404:
            print("Bucket Does Not Exist!")
            return False

def upload_data_in_S3(record_response):
    bucketExists = check_bucket(bucket_name)
    if bucketExists:
        name = get_filename_datetime()
        path = create_File(name,record_response)
        s3.Object(bucket_name, path).put(Body=open(path, 'rb'))
    else:
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.create_bucket(Bucket=bucket_name)
        name = get_filename_datetime()
        path =  create_File(name, record_response)
        s3.Object(bucket_name, path).put(Body=open(path, 'rb'))
#UTILITY FUNCTIONS ENDS HERE


#MAIN BUISNESS CODD STARTS HERE
kinesis_client = boto3.client('kinesis', region_name='us-east-1')
response = kinesis_client.describe_stream(StreamName=my_stream_name)
my_shard_id = response['StreamDescription']['Shards'][0]['ShardId']
shard_iterator = kinesis_client.get_shard_iterator(StreamName=my_stream_name,
                                                      ShardId=my_shard_id,
                                                      ShardIteratorType='LATEST')

my_shard_iterator = shard_iterator['ShardIterator']
record_response = kinesis_client.get_records(ShardIterator=my_shard_iterator,
                                              Limit=2)
while 'NextShardIterator' in record_response:
    record_response = kinesis_client.get_records(ShardIterator=record_response['NextShardIterator'],
                                                  Limit=2)
    upload_data_in_S3(record_response)
    time.sleep(5)
#MAIN BUISNESS CODD ENDS HERE