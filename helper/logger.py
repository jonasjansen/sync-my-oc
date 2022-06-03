import datetime

from helper.configuration_provider import ConfigurationProvider


class Logger:
    LOGGER_FILE_NAME = '.oc-sync-log.txt'
    configuration: ConfigurationProvider = None

    def __init__(self, configuration):
        self.configuration = configuration

    def log(self, *text):
        try:
            if self.configuration.get_configuration(self.configuration.CONFIG_KEY_ENABLE_LOGGING):
                content = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' - '
                for text_part in text:
                    content += str(text_part)
                content += '\n'
                file = open(self.LOGGER_FILE_NAME, 'a+')
                file.write(content)
        except Exception as error:
            print("Fehler beim Loggen:", error)
