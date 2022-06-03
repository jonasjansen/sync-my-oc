import json
import hashlib
from typing import Dict

from helper.logger import Logger


class Cache:
    FILE_CACHE_FILE_NAME = ".oc-sync-file-cache.json"

    downloaded_files: Dict[str, Dict] = None
    logger = None

    def __init__(self, logger: Logger):
        self.logger = logger
        self.downloaded_files = dict()
        pass

    def add_downloaded_file(self, file_name, file_path, file_hash, upload_date):
        hash_id = self.generate_hash_id_from_text(str(file_path))
        self.downloaded_files[hash_id] = {
            'name': str(file_name),
            'local_file_path': str(file_path),
            'local_file_hash': str(file_hash),
            'upload_date': str(upload_date)
        }
        self.write_cache()

    def read_cache(self):
        try:
            with open(self.FILE_CACHE_FILE_NAME) as json_data_file:
                data = json.load(json_data_file)
            self.downloaded_files = data
        except Exception as error:
            self.logger.log("Fehler beim Lesen des File-Caches: ", error)
        return self.downloaded_files

    def write_cache(self):
        with open(self.FILE_CACHE_FILE_NAME, 'w') as outfile:
            json.dump(self.downloaded_files, outfile)
            outfile.close()

    def generate_hash_id_from_text(self, text: str):
        hash_id = str(int(hashlib.md5(text.encode("utf-8")).hexdigest(), 16))
        return hash_id
