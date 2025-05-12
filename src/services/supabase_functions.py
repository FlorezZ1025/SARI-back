from datetime import datetime
from supabase import StorageException
from werkzeug.utils import secure_filename
from src.utils.db import s3
from werkzeug.datastructures import FileStorage

def upload_pdf_to_supabase(file_storage:FileStorage):
    
    try:
        s3.upload_fileobj(
            file_storage,
            'evidences-pdfs',
            file_storage.filename,
            ExtraArgs={'ContentType': 'application/pdf'}
        )
        print(f"Archivo {file_storage} subido correctamente como {file_storage.filename}.")
        return "https://zeklgcmdroygkrjrcimi.supabase.co/storage/v1/object/public/evidences-pdfs/" + file_storage.filename
    except Exception as e:
        print(f"Error al subir el archivo: {e}")
        return False
