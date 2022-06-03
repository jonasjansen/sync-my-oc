import hashlib
import os

from PyQt5.QtCore import QThread, pyqtSignal
from pathlib import Path

from helper.cache import Cache


class Downloader(QThread):
    """
    Runs a counter thread.
    """
    countChanged = pyqtSignal(int)
    finished_signal = pyqtSignal(str)
    session = None
    files_to_download = None
    directoryPath = None
    overwrite_existing_files = None
    logger = None
    cache = None

    def __init__(self, logger, parent=None):
        super(self.__class__, self).__init__(parent)
        self.logger = logger

    def run(self):
        file_count = len(self.files_to_download)

        if file_count:
            step_size = 100 / file_count
            progress = 0

            for file_name in self.files_to_download.keys():
                self.logger.log("Download Datei ", self.files_to_download[file_name])
                current_file = self.files_to_download[file_name]
                r = self.session.get(current_file['url'], allow_redirects=True)
                file_directory = Path(
                    self.directoryPath.text(),
                    current_file['additional_file_path']
                )
                file_directory.mkdir(parents=True, exist_ok=True)
                file_path = Path(file_directory, file_name)

                if not os.path.exists(file_path) or self.overwrite_existing_files:
                    try:
                        file = open(file_path, 'wb')
                        file.write(r.content)
                        file.close()
                        file_hash = self.get_file_hash(str(file_path))
                        self.cache.add_downloaded_file(
                            str(file_name),
                            str(file_path),
                            str(file_hash),
                            str(current_file['uploaded_date'])
                        )
                    except Exception as error:
                        self.logger.log("Datei", file_path, "kann nicht gespeichert werden:", error)

                progress += step_size
                self.countChanged.emit(progress)

        self.finished_signal.emit('Download beendet')

    def get_file_hash(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def set_session(self, session):
        self.session = session

    def set_files_to_download(self, files_to_download):
        self.files_to_download = files_to_download

    def set_directory_path(self, directory_path):
        self.directoryPath = directory_path

    def set_override_existing_files(self, overwrite_existing_files):
        self.overwrite_existing_files = overwrite_existing_files

    def set_cache(self, cache: Cache):
        self.cache = cache
