import os
from PyQt5 import QtWidgets, QtCore, QtGui
from pathlib import Path

from gui.color_code_info import ColorCodeInfo
from gui.message_box import MessageBox
from helper.cache import Cache
from helper.configuration_provider import ConfigurationProvider
from helper.downloader import Downloader
from crawler.website_client import WebsiteClient
from gui.layouts import main_form
from crawler.crawler import Crawler
from gui.progress_dialog import ProgressDialog
from helper.logger import Logger


class MainForm(QtWidgets.QMainWindow, main_form.Ui_MainWindow):
    COLUMN_INFORMATION = 0
    COLUMN_FILE_NAME = 1
    COLUMN_DOWNLOAD_URL = 2
    COLUMN_ADDITIONAL_FILE_PATH = 3
    COLUMN_UPLOADED_DATE = 4
    SEMESTER_DEFAULT_TEXT = 'Keine Daten vorhanden'

    logger = None
    website_client = None
    courses = None
    semester_names = list()
    semester_alternative_names = list()
    semesters = dict()

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # Window Icon
        self.setWindowIcon(QtGui.QIcon('gui/icon.jpg'))

        # Initialize class attributes
        self.progress_dialog = ProgressDialog()
        self.semesters = dict()
        self.configuration = ConfigurationProvider()
        self.logger = Logger(self.configuration)
        self.cache = Cache(self.logger)
        self.website_client = WebsiteClient(self.logger)
        self.crawler = Crawler(self.logger)
        self.downloader = Downloader(self.logger)

        # Replace dummy button with QCombobox because it is not included in the designer
        self.dummyButton.hide()
        self.semesterSelectButton = QtWidgets.QComboBox(self.tab)
        self.semesterSelectButton.setObjectName("semesterSelectButton")
        self.semesterSelectButton.setMinimumHeight(30)
        self.gridLayout_3.addWidget(self.semesterSelectButton, 0, 0, 1, 1)

        # Additional Forms
        self.message_box = MessageBox()
        self.color_code_information = ColorCodeInfo()

        # Connect buttons with function
        # Functional Buttons
        self.syncButton.clicked.connect(self.synchronizing_start)
        self.downloadButton.clicked.connect(self.download_start)
        self.selectDirectoryButton.clicked.connect(self.select_directory)
        self.semesterSelectButton.activated.connect(self.changed_combo_box)
        self.colorLegendButton.clicked.connect(self.color_code_information.show)

        # Config checkboxes and radio buttons
        self.checkBox_all_semesters.clicked.connect(
            self.update_configuration_check_box(self.checkBox_all_semesters, self.configuration.CONFIG_KEY_ALL_SEMESTERS))
        self.checkBox_show_events.clicked.connect(
            self.update_configuration_check_box(self.checkBox_show_events, self.configuration.CONFIG_KEY_SHOW_EVENTS, True))
        self.checkBox_semester_as_folder.clicked.connect(
            self.update_configuration_check_box(self.checkBox_semester_as_folder, self.configuration.CONFIG_KEY_SEMESTER_AS_FOLDER))
        self.checkBox_course_as_folder.clicked.connect(
            self.update_configuration_check_box(self.checkBox_course_as_folder, self.configuration.CONFIG_KEY_COURSE_AS_FOLDER))
        self.checkBox_lecturer_as_folder.clicked.connect(
            self.update_configuration_check_box(self.checkBox_lecturer_as_folder, self.configuration.CONFIG_KEY_LECTURER_AS_FOLDER))
        self.checkBox_overwrite_existing_files.clicked.connect(
            self.update_configuration_check_box(self.checkBox_overwrite_existing_files, self.configuration.CONFIG_KEY_OVERWRITE_EXISTING_FILES))
        self.checkBox_enable_loggin.clicked.connect(
            self.update_configuration_check_box(self.checkBox_enable_loggin, self.configuration.CONFIG_KEY_ENABLE_LOGGING))
        self.radioButton_semester_naming_v1.clicked.connect(self.update_configuration_radio_button)
        self.radioButton_semester_naming_v2.clicked.connect(self.update_configuration_radio_button)

        # Set default values
        self.directoryPath.setText(os.getcwd())
        self.treeItems.hideColumn(self.COLUMN_DOWNLOAD_URL)
        self.treeItems.hideColumn(self.COLUMN_ADDITIONAL_FILE_PATH)
        self.treeItems.hideColumn(self.COLUMN_UPLOADED_DATE)
        self.checkBox_semester_as_folder.setChecked(True)
        self.checkBox_course_as_folder.setChecked(True)
        self.radioButton_semester_naming_v1.setChecked(True)
        self.semesterSelectButton.addItem(self.SEMESTER_DEFAULT_TEXT)
        self.progress_dialog.progressBar.setValue(0)

        self.init_configuration()

    def init_configuration(self):
        self.directoryPath.setText(
            self.configuration.get_configuration(self.configuration.CONFIG_KEY_DIRECTORY_PATH)
        )
        self.checkBox_all_semesters.setChecked(
            self.configuration.get_configuration(self.configuration.CONFIG_KEY_ALL_SEMESTERS)
        )
        self.checkBox_show_events.setChecked(
            self.configuration.get_configuration(self.configuration.CONFIG_KEY_SHOW_EVENTS)
        )
        self.checkBox_semester_as_folder.setChecked(
            self.configuration.get_configuration(self.configuration.CONFIG_KEY_SEMESTER_AS_FOLDER)
        )
        self.checkBox_course_as_folder.setChecked(
            self.configuration.get_configuration(self.configuration.CONFIG_KEY_COURSE_AS_FOLDER)
        )
        self.checkBox_lecturer_as_folder.setChecked(
            self.configuration.get_configuration(self.configuration.CONFIG_KEY_LECTURER_AS_FOLDER)
        )
        self.checkBox_overwrite_existing_files.setChecked(
            self.configuration.get_configuration(self.configuration.CONFIG_KEY_OVERWRITE_EXISTING_FILES)
        )
        self.checkBox_enable_loggin.setChecked(
            self.configuration.get_configuration(self.configuration.CONFIG_KEY_ENABLE_LOGGING)
        )
        self.radioButton_semester_naming_v1.setChecked(
            self.configuration.get_configuration(self.configuration.CONFIG_KEY_SEMESTER_NAMING_V1)
        )
        self.radioButton_semester_naming_v2.setChecked(
            self.configuration.get_configuration(self.configuration.CONFIG_KEY_SEMESTER_NAMING_V2)
        )

    def update_configuration_check_box(self, checkbox, config_key, update_tree_table=False):
        def update_configuration():
            self.configuration.set_configuration(config_key, checkbox.isChecked())
            if update_tree_table:
                self.update_tree_table()
        return update_configuration

    def update_configuration_radio_button(self):
        self.configuration.set_configuration(
            self.configuration.CONFIG_KEY_SEMESTER_NAMING_V1,
            self.radioButton_semester_naming_v1.isChecked()
        )
        self.configuration.set_configuration(
            self.configuration.CONFIG_KEY_SEMESTER_NAMING_V2,
            self.radioButton_semester_naming_v2.isChecked()
        )
        self.update_semester_data()

    def changed_combo_box(self):
        self.update_tree_table()
        return

    def synchronizing_start(self):
        try:
            self.logger.log("Start der Sychronisierung")
            self.crawler.set_session(self.website_client.get_login_session())
            self.crawler.set_start_page_url(self.website_client.get_start_page_url())
            self.crawler.set_configuration(self.configuration)
            self.crawler.finished_signal.connect(self.synchronizing_finished)
            self.message_box.set_text("Synchronisierung", "Synchronisiere Online Campus...")
            self.message_box.set_running_thread(self.crawler)
            self.message_box.show()
            self.crawler.start()

        except Exception as error:
            self.logger.log("Fehler beim Synchronisieren: " + str(error))
            self.message_box.set_text("Fehler beim Synchronisieren", str(error))
            self.message_box.show()
            self.semesterSelectButton.addItem(self.SEMESTER_DEFAULT_TEXT)
        return

    def synchronizing_finished(self, message):
        try:
            self.logger.log(message)
            self.process_semester_data(self.crawler.semester_data)
            self.update_semester_data()
            self.update_tree_table()
            self.message_box.hide()

        except Exception as error:
            self.logger.log("Fehler in den synchronisierten Semesterdaten: ", error)
            self.semesterSelectButton.addItem(self.SEMESTER_DEFAULT_TEXT)

    def process_semester_data(self, semester_data: []) -> None:
        """
        Clears existing semester data.
        Saves semester names and alternative names into self.semesters dictionary.
        Adds semesters names and alternative names to lists.
        :param semester_data:
        :return:
        """
        self.semesterSelectButton.clear()
        self.semesters.clear()
        self.semester_names.clear()
        self.semester_alternative_names.clear()

        for semester in semester_data:
            self.semester_names.append(semester.semester_name)
            self.semester_alternative_names.append(semester.semester_alternative_name)
            self.semesters[semester.semester_name] = semester
            self.semesters[semester.semester_alternative_name] = semester
        return

    def update_semester_data(self):
        self.semesterSelectButton.clear()
        if self.configuration.get_configuration(self.configuration.CONFIG_KEY_SEMESTER_NAMING_V1):
            for semester_name in self.semester_names:
                self.semesterSelectButton.addItem(semester_name)
        else:
            for semester_name in self.semester_alternative_names:
                self.semesterSelectButton.addItem(semester_name)
        return

    def update_tree_table(self):
        """
        :param courses: list
        :return:
        """
        try:
            semester = self.semesters[ self.semesterSelectButton.currentText() ]
        except Exception as error:
            self.logger.log("Kein gültiges Semester ausgewählt oder keine Daten vorhanden: ", error)
            return

        if semester:
            self.treeItems.clear()
            self.logger.log("Adding courses")
            for course in semester.course_list:
                """:var course: Course"""
                # Save course lecturer in 3rd invisible column
                course_item = QtWidgets.QTreeWidgetItem(self.treeItems, [course.course_name, '', course.course_lecturer])
                course_item.setFlags(course_item.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                course_item.setCheckState(0, QtCore.Qt.Unchecked)
                additional_file_path = self.get_additional_file_path(course)

                for event in course.event_list:
                    """:var event: Event"""
                    if self.configuration.get_configuration(self.configuration.CONFIG_KEY_SHOW_EVENTS):

                        event_item = QtWidgets.QTreeWidgetItem(course_item, [event.event_name])
                        event_item.setFlags(
                            event_item.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                        event_item.setCheckState(0, QtCore.Qt.Unchecked)
                        parent_item = event_item
                    else:
                        parent_item = course_item

                    self.add_material_to_tree(event.material_list, parent_item, additional_file_path)

    def get_additional_file_path(self, course):
        additional_file_path = ''
        if (self.configuration.get_configuration(self.configuration.CONFIG_KEY_SEMESTER_AS_FOLDER)):
            additional_file_path = additional_file_path + self.semesterSelectButton.currentText() + '/'

        if (self.configuration.get_configuration(self.configuration.CONFIG_KEY_COURSE_AS_FOLDER)):
            additional_file_path = additional_file_path + course.course_name + '/'

        if (self.configuration.get_configuration(self.configuration.CONFIG_KEY_LECTURER_AS_FOLDER)):
            additional_file_path = additional_file_path + course.course_lecturer + '/'

        return additional_file_path

    def add_material_to_tree(self, material_list, parent_item, additional_file_path):
        for material in material_list:
            """:var material: Material"""
            try:
                material_item = QtWidgets.QTreeWidgetItem(
                    parent_item,
                    [
                        material.name,
                        material.file_name,
                        material.download_url,
                        additional_file_path,
                        material.upload_date
                    ]
                )
                color = self.get_color(material.file_name, additional_file_path, material.upload_date)
                material_item.setForeground(0, color)
                material_item.setForeground(1, color)
                material_item.setFlags(material_item.flags() | QtCore.Qt.ItemIsUserCheckable)
                material_item.setCheckState(0, QtCore.Qt.Unchecked)
            except Exception as error:
                print(error)
                self.logger.log(error)
        return

    def get_color(self, file_name, additional_file_path, upload_date):
        file_changed_online = False
        file_changed_local = False

        file_path = Path(self.directoryPath.text(), additional_file_path, file_name)
        file_exists = os.path.exists(file_path)
        hash_id = self.cache.generate_hash_id_from_text(str(file_path))
        #Todo: Do not read the cache for every file, only once per download.
        # Maybe pass previous downloaded files as argument.
        previous_downloaded_files = self.cache.read_cache()
        try:
            current_previous_downloaded_file = previous_downloaded_files[hash_id]
            if current_previous_downloaded_file['upload_date'] != upload_date:
                file_changed_online = True
            if current_previous_downloaded_file['local_file_hash'] != self.downloader.get_file_hash(file_path):
                file_changed_local = True
        except Exception as error:
            self.logger.log(error)

        if file_changed_local and file_changed_online:
            return QtGui.QColor("violet")
        if file_changed_local:
            return QtGui.QColor("red")
        if file_changed_online:
            return QtGui.QColor("blue")
        if file_exists:
            return QtGui.QColor("orange")

        return QtGui.QColor("green")

    def download_start(self):
        try:
            self.progress_dialog.show()
            self.downloader.set_cache(self.cache)
            self.downloader.set_session(self.website_client.get_login_session())
            self.downloader.set_files_to_download(self.get_selected_download_files())
            self.downloader.set_directory_path(self.directoryPath)
            self.downloader.set_override_existing_files(
                self.configuration.get_configuration(self.configuration.CONFIG_KEY_OVERWRITE_EXISTING_FILES)
            )
            self.downloader.countChanged.connect(self.on_count_changed)
            self.downloader.finished_signal.connect(self.download_finished)
            self.downloader.start()

        except Exception as error:
            self.logger.log("Fehler beim Download: " + str(error))
            self.message_box.set_text("Fehler beim Download", str(error))
            self.message_box.show()
        return

    def on_count_changed(self, value):
        self.progress_dialog.progressBar.setValue(value)

    def download_finished(self, message):
        self.logger.log(message)
        self.progress_dialog.hide()
        self.progress_dialog.progressBar.setValue(0)
        self.update_tree_table()
        return

    def get_selected_download_files(self):
        urls_to_download = dict()
        root = self.treeItems.invisibleRootItem()
        course_count = root.childCount()

        for i in range(course_count):
            course = root.child(i)
            if self.configuration.get_configuration(self.configuration.CONFIG_KEY_SHOW_EVENTS):
                event_count = course.childCount()

                for k in range(event_count):
                    event = course.child(k)
                    urls_to_download = self.get_selected_material(event, urls_to_download)
            else:
                urls_to_download = self.get_selected_material(course, urls_to_download)

        return urls_to_download

    def get_selected_material(self, parent, urls_to_download):
        material_count = parent.childCount()

        for l in range(material_count):
            material = parent.child(l)
            if material.checkState(0) == QtCore.Qt.Checked \
                    and material.text(self.COLUMN_FILE_NAME) is not None \
                    and material.text(self.COLUMN_DOWNLOAD_URL) is not None \
                    and material.text(self.COLUMN_ADDITIONAL_FILE_PATH) is not None:
                urls_to_download[material.text(1)] = {
                    'url': material.text(self.COLUMN_DOWNLOAD_URL),
                    'additional_file_path': material.text(self.COLUMN_ADDITIONAL_FILE_PATH),
                    'uploaded_date': material.text(self.COLUMN_UPLOADED_DATE)}
        return urls_to_download

    def select_directory(self):
        file_dialog = QtWidgets.QFileDialog()
        file_name = file_dialog.getExistingDirectory()
        self.configuration.set_configuration(self.configuration.CONFIG_KEY_DIRECTORY_PATH, file_name)
        self.directoryPath.setText(file_name)
        return
