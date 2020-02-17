import boto3
import json
from datetime import datetime
import calendar
import random


kinesisClient = boto3.client('kinesis', region_name='us-east-1')

while True:
    property_value = random.randint(40, 120)
    property_timestamp = calendar.timegm(datetime.utcnow().timetuple())
    thing_id = 'amazon-assignment'

    payload = {
        'prop': str(property_value),
        'timestamp': str(property_timestamp),
        'thing_id': thing_id
    }

    put_response = kinesisClient.put_record(StreamName='aws-training-umartahir',
                                            Data=json.dumps(payload),PartitionKey=thing_id)

    print(put_response)

