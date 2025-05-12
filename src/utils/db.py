import boto3
from flask_sqlalchemy import SQLAlchemy
from botocore.client import Config
import os
from dotenv import load_dotenv
load_dotenv()

ENDOPOINT_SUP_S3 = os.getenv('ENDPOINT_SUP_S3')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
# BUCKET_NAME = 'evidences-pdfs'
print(ENDOPOINT_SUP_S3)
print(AWS_ACCESS_KEY_ID)
s3 = boto3.client(
    's3',
    endpoint_url=ENDOPOINT_SUP_S3,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    config=Config(signature_version='s3v4'),
    region_name='us-east-2'
)
db = SQLAlchemy()