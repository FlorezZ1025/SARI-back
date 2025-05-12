import boto3
from flask_sqlalchemy import SQLAlchemy
from botocore.client import Config
import os

# from supabase import create_client

sup_url = "https://zeklgcmdroygkrjrcimi.supabase.co/storage/v1/s3"
sup_key = os.getenv('SUPABASE_KEY')

BUCKET_NAME = 'evidences-pdfs'

s3 = boto3.client(
    's3',
    endpoint_url=sup_url,
    aws_access_key_id='a224e74be5d8dc4a5cc22d3f487c5602',  # 'sb' es el valor por defecto para Supabase
    aws_secret_access_key='4fff9d3e853f8da14d281d3d6a18acdcca5042c581319a6e7da9c4e33692abca',
    config=Config(signature_version='s3v4'),
    region_name='us-east-2'  # Puede ser cualquier región, Supabase lo ignora
)



# supabase = create_client(sup_url, sup_key)

db = SQLAlchemy()