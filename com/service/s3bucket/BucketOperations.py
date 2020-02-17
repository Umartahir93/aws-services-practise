import boto3

#create bucket
s3 = boto3.resource('s3')
bucket = s3.create_bucket(Bucket='awstraining.umartahir.practisetask')


#upload object
s3.Object('awstraining.umartahir.practisetask', 'image.png').put(Body=open('image.png', 'rb'))


#download object
s3Client = boto3.client('s3')
s3Client.download_file('awstraining.umartahir.practisetask', 'image.png', 'downloaded_Image.png')


#delee keys and bucket
for key in bucket.objects.all():
    key.delete()


bucket.delete()