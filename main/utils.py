from cchardet import UniversalDetector
import csv
import magic
import pandas as pd
import os
from main.logger import get_logger
import tempfile


tmp_dir = None

logger = get_logger(__name__)

def detect_encoding(file):
    detector = UniversalDetector()
    detector.reset()
    with open(file, 'rb') as f:
        for row in f:
            detector.feed(row)
            if detector.done:
                break
    detector.close()
    return detector.result

def looks_like_csv(file):
    try:
        encoding = detect_encoding(file)
        with open(file, encoding=encoding['encoding']) as f:
            content = f.read()
            if content.lower().startswith('<!doctype html'):
                return False
            csv.Sniffer().sniff(content)
            return True
    except Exception as e:  # noqa
        return False


def extract_data(path):
    if looks_like_csv(path):
        media_type = 'text/csv'
    else:
        path = convert_to_csv(path)

    return path


def convert_to_csv(path):
    media_type = magic.from_file(path, mime=True)
    tmp_path = csv_path(tmp_dir, path)

    try:
        excel = pd.read_excel(path)
    except:
        excel = None

    if excel is not None:
        excel.to_csv(tmp_path, index=None, header=True)
        return tmp_path

    logger.info(f"Unable to convert {path} from {media_type} to CSV")
    with open(tmp_path, 'w') as out:
        pass
    return tmp_path


def csv_path(_dir, path):
    path = os.path.join(_dir, basename(path)) if _dir else path
    return path + ".csv"


def basename(p):
    """Returns the final component of a pathname"""
    p = os.fspath(p)
    sep = _get_sep(p)
    i = p.rfind(sep) + 1
    return p[i:]


def _get_sep(path):
    if isinstance(path, bytes):
        return b'/'
    else:
        return '/'
    
def save_uploaded_file(file):
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, file.filename)
    file.file.seek(0)
    #contents = file.file.read().decode("utf-8")
    with open(temp_file_path, 'wb') as temp_file:
        temp_file.write(file.file.read())
    return temp_file_path