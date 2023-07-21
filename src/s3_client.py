import config
import os

import boto3
from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError, WaiterError

AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
REGION_NAME = config.REGION_NAME

s3_client = boto3.client(
    's3',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = REGION_NAME
)

session = boto3.Session(
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name = REGION_NAME
)
s3_resource = session.resource('s3')


# Create s3 bucket per session (ex: Folder for Files)
def create_session_bucket(session_id):   
    bucket_response = s3_client.create_bucket(
        Bucket = f'session-{session_id}',
        CreateBucketConfiguration={
            'LocationConstraint': REGION_NAME
        },        
    )
    return bucket_response


def upload_object_to_bucket(session_id, file_obj):
    file_name = secure_filename(file_obj.filename)

    try:
        bucket = s3_resource.Bucket(session_id)
    except ClientError as e:
        return f"Error occured when trying to locate s3 bucket: {e}"
    
    s3_client.upload_fileobj(
        file_obj,
        session_id,
        file_name
    )

    try:
        s3_resource.Object(session_id, file_name).wait_until_exists()
    except WaiterError as e:
        return f"Error occurent when waiting for file to upload: {e}"
    else:
        head_object = s3_client.head_object(Bucket=session_id, Key=file_name)
        response = head_object

    return response


def get_object(session_id, object_name, path):
    # object = s3_client.get_object(
    #     Bucket=session_id,
    #     Key=object_name,
    # )
    path_name = path + session_id + object_name
    response = s3_client.download_file(session_id, object_name, path_name)
    # TODO: Need to check progress of download file/latency
    if os.path.exists(path_name):
        return f"Successfully downloaded {object_name} to {path_name}"
    return "Failed to download_file"


# To update an object, you simply upload to bucket with same key(object_name)


def delete_object(session_id, object_name):
    response = s3_client.delete_object(
        Bucket=session_id,
        Key=object_name,
    )

    return response


def delete_bucket(session_id):
    response = s3_client.delete_bucket (
        Bucket = session_id
    )

    return response
