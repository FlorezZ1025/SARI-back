from datetime import datetime
import re
from urllib.parse import urlparse
from supabase import StorageException
from werkzeug.utils import secure_filename
from src.utils.db import s3
from werkzeug.datastructures import FileStorage
from dotenv import load_dotenv
import os
load_dotenv()
BUCKET_NAME = os.getenv('BUCKET_NAME')
BUCKET_URL = os.getenv('BUCKET_URL')

def upload_pdf_to_supabase(file_storage:FileStorage):
    orginal_filename = secure_filename(file_storage.filename)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_name = f"{timestamp}_{orginal_filename}"
    # unique_name = 
    try:
        s3.upload_fileobj(
            file_storage,
            BUCKET_NAME,
            unique_name,
            ExtraArgs={'ContentType': 'application/pdf'}
        )
        print(f"Archivo {file_storage} subido correctamente como {unique_name}.")
        return BUCKET_URL + unique_name
    except Exception as e:
        print(f"Error al subir el archivo: {e}")
        return False
    
def get_object_key_from_url(url):
    """Extrae la clave S3 desde la URL pública de Supabase"""
    parsed = urlparse(url)
    path = parsed.path
    
    patterns = [
        r'/storage/v1/object/public/([^/]+)/(.+)',  # URL pública
        r'/storage/v1/object/sign/([^/]+)/(.+)\?',  # URL firmada
    ]
    
    for pattern in patterns:
        match = re.search(pattern, path)
        if match and match.group(1) == 'evidences-pdfs':
            return match.group(2)
    
    return None