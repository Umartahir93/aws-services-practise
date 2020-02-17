#============== This is not correct solution as I am not able to understand how to get
#               query parameters through SAM template.yml
#               and how to modify lambda that
#               it accepts query parametersss ===================


import boto3,botocore

def lambda_handler(event, context):

    bucket_name = 'aws-training-umartahir-sam-assigmnment'
    s3 = boto3.resource('s3')

    try:
        s3.Object(bucket_name, event['filename']).load()

    except botocore.exceptions.ClientError as e:

        if e.response['Error']['Code'] == "404":
            print("File Does not exists")
        else:
            print("Object in s3 added")
    else:
        print("File exists")


