from cchardet import UniversalDetector
import csv
import magic
import pandas as pd
import os
from components.logger import get_logger
import tempfile
import hashlib
import subprocess


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
    except Exception as e:
        logger.error("Exception occured while scanning the file: %s", str(e))  
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

    logger.error(f"Unable to convert {path} from {media_type} to CSV")
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
    try:
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, file.filename)
        file.file.seek(0)
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(file.file.read())
    except Exception as e:
        logger.error("Unable to save file: %s", str(e))
    return temp_file_path

def save_content(content):
        temp_dir = tempfile.mkdtemp()
        resource = hashlib.sha256(content).hexdigest()
        path = os.path.join(temp_dir, resource)
        with open(path, 'wb') as temp_file:
            temp_file.write(content)
        return temp_file

def save_contents_to_file(contents):
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, "arcgistemp")
    try:
        with open(temp_file_path, 'wb') as file:
            file.write(contents)
        print("Contents saved to", temp_file_path)
        return temp_file_path  # Return the file path after successful save
    except IOError as e:
        print("Error saving contents:", str(e))
        return None  # Return None if there was an error




def execute(command):
    logger.debug("execute: %s", command)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        outs, errs = proc.communicate(timeout=600)
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()

    return proc.returncode, outs.decode("utf-8"), errs.decode("utf-8")


def convert_features_to_csv(input_path):
    output_path = tempfile.NamedTemporaryFile(suffix=".csv").name
    execute(
        [
            "ogr2ogr",
            "-oo",
            "DOWNLOAD_SCHEMA=NO",
            "-lco",
            "GEOMETRY=AS_WKT",
            "-lco",
            "LINEFORMAT=CRLF",
            "-f",
            "CSV",
            "-nlt",
            "MULTIPOLYGON",
            "-nln",
            "MERGED",
            "--config",
            "OGR_WKT_PRECISION",
            "10",
            output_path,
            input_path,
        ]
    )
    if not os.path.isfile(output_path):
        return None

    return output_path

def read_csv(input_path, encoding="utf-8"):
    logger.debug("reading %s with encoding %s", input_path, encoding)
    return open(input_path, encoding=encoding, newline=None)

def _read_text_file( input_path, encoding, charset):
        f = read_csv(input_path, encoding)
        #self.log.mime_type = "text/csv" + self.charset
        content = f.read(10)
        f.seek(0)
        converted_csv_file = None

        if content.lower().startswith("<!doctype "):
            #self.log.mime_type = "text/html" + self.charset
            logger.warn("%s has <!doctype, IGNORING!", input_path)
            f.close()
            return None

        elif content.lower().startswith(("<?xml ", "<wfs:")):
            logger.debug("%s looks like xml", input_path)
            #self.log.mime_type = "application/xml" + self.charset
            converted_csv_file = convert_features_to_csv(input_path)
            if not converted_csv_file:
                f.close()
                logger.warning("conversion from XML to CSV failed")
                return None

        elif content.lower().startswith("{"):
            logger.debug("%s looks like json", input_path)
            #self.log.mime_type = "application/json" + self.charset
            converted_csv_file = convert_features_to_csv(input_path)

        if converted_csv_file:
            f.close()
            reader = read_csv(converted_csv_file)
        else:
            reader = f

        return converted_csv_file


def detect_file_encoding(path):
    with open(path, "rb") as f:
        return detect_encoding(f)


def detect_encoding(f):
    detector = UniversalDetector()
    detector.reset()
    for line in f:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result["encoding"]