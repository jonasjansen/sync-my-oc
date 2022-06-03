import json
import os
from typing import Dict, Any


class ConfigurationProvider:
    CACHE_FILE_NAME = ".oc-sync-config-cache.json"

    CONFIG_KEY_DIRECTORY_PATH = "directory_path"
    CONFIG_KEY_ALL_SEMESTERS = "all_semesters"
    CONFIG_KEY_SHOW_EVENTS = "show_events"
    CONFIG_KEY_SEMESTER_AS_FOLDER = "semester_as_folder"
    CONFIG_KEY_COURSE_AS_FOLDER = "course_as_folder"
    CONFIG_KEY_LECTURER_AS_FOLDER = "lecturer_as_folder"
    CONFIG_KEY_OVERWRITE_EXISTING_FILES = "overwrite_existing_files"
    CONFIG_KEY_ENABLE_LOGGING = "enable_logging"
    CONFIG_KEY_SEMESTER_NAMING_V1 = "semester_naming_v1"
    CONFIG_KEY_SEMESTER_NAMING_V2 = "semester_naming_v2"

    configuration: Dict[str, any] = None

    def __init__(self):
        self.configuration = dict()
        if os.path.exists(self.CACHE_FILE_NAME):
            self.read_config_cache()

        else:
            self.set_all_configuration(
                {
                    self.CONFIG_KEY_DIRECTORY_PATH: os.getcwd(),
                    self.CONFIG_KEY_ALL_SEMESTERS: False,
                    self.CONFIG_KEY_SHOW_EVENTS: False,
                    self.CONFIG_KEY_SEMESTER_AS_FOLDER: True,
                    self.CONFIG_KEY_COURSE_AS_FOLDER: True,
                    self.CONFIG_KEY_LECTURER_AS_FOLDER: False,
                    self.CONFIG_KEY_OVERWRITE_EXISTING_FILES: False,
                    self.CONFIG_KEY_ENABLE_LOGGING: False,
                    self.CONFIG_KEY_SEMESTER_NAMING_V1: True,
                    self.CONFIG_KEY_SEMESTER_NAMING_V2: False,
                }
            )

    def set_configuration(self, key: str, value: any):
        self.configuration[key] = value
        self.write_config_cache()

    def get_configuration(self, key: str) -> any:
        if key in self.configuration:
            return self.configuration[key]
        else:
            return None

    def get_all_configuration(self) -> {str: any}:
        return self.configuration

    def set_all_configuration(self, new_configuration: {str: any}):
        for key in new_configuration.keys():
            self.configuration[key] = new_configuration[key]
        self.write_config_cache()

    def read_config_cache(self):
        if os.path.exists(self.CACHE_FILE_NAME):
            with open(self.CACHE_FILE_NAME) as json_data_file:
                data = json.load(json_data_file)
            self.configuration = data

    def write_config_cache(self):
        with open(self.CACHE_FILE_NAME, 'w') as outfile:
            json.dump(self.configuration, outfile)
            outfile.close()
