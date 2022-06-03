import re

from PyQt5.QtCore import QThread, pyqtSignal

from crawler.website_client import WebsiteClient
from entities.course import Course
from bs4 import BeautifulSoup, Tag

from entities.event import Event
from entities.material import Material
from entities.semester import Semester
from gui.message_box import MessageBox
from helper.configuration_provider import ConfigurationProvider
from helper.logger import Logger


class Crawler(QThread):

    def __init__(self, logger, parent=None):
        super(self.__class__, self).__init__(parent)
        self.logger = logger

    SEMESTER_SUFFIX = ". Semester"

    finished_signal = pyqtSignal(str)

    semesters = list()
    session = None
    start_page_url = None
    configuration: ConfigurationProvider = None
    logger: Logger = None
    semester_data = None

    def set_session(self, session):
        self.session = session

    def set_start_page_url(self, start_page_url):
        self.start_page_url = start_page_url

    def set_configuration(self, configuration):
        self.configuration = configuration

    def run(self):
        try:
            self.crawl()

        except Exception as error:
            self.logger.log("Error when crawling the website: ", error)

        self.finished_signal.emit('Synchronisierung beendet')

    def get_page_soup(self, url):
        """
        :param url: string
        :return: BeautifulSoup
        """
        self.logger.log("Crawling: ", url)
        if self.session:
            page_content = self.session.get(url)
            return BeautifulSoup(page_content.content, 'html.parser')
        else:
            return None

    def crawl(self):
        if self.start_page_url:
            soup = self.get_page_soup(self.start_page_url)
            html_element = soup.find("a", string="Meine Veranstaltungen")

            if html_element is not None:
                course_overview_url = html_element['href']
                self.semester_data = self.get_semesters(WebsiteClient.BASE_URL + course_overview_url)
            else:
                self.logger.log("Meine Veranstaltungen konnte auf der Website nicht gefunden werden!")

        return None

    def get_semesters(self, first_course_overview_url):
        semester_data = dict()
        semesters = list()

        try:
            soup = self.get_page_soup(first_course_overview_url)
            html_element_scroller: Tag = soup.find("div", attrs={'class': "semester-scroller"})
            active_semester_name = html_element_scroller.find("a", attrs={"class": "aktiv"}).text

            for link in html_element_scroller.find_all('a'):
                semester_soup = self.get_page_soup(WebsiteClient.BASE_URL + link['href'])
                if semester_soup.find("table", attrs={'class': "tablesorter"}):
                    semester_data[link.text] = semester_soup

            semester_count = len( semester_data )

            # Todo: rename property into only current semester
            if not self.configuration.get_configuration(self.configuration.CONFIG_KEY_ALL_SEMESTERS):
                semester_data = {active_semester_name: semester_data[active_semester_name]}

            for semester_name in semester_data.keys():
                semester_courses = self.get_courses(semester_data[semester_name])
                if semester_courses:
                    semester_alternative_name = str(semester_count) + self.SEMESTER_SUFFIX
                    semesters.append( Semester(semester_name, semester_alternative_name, semester_courses ) )
                semester_count -= 1

        except Exception as error:
            self.logger.log(error)
        return semesters

    def get_courses(self, semester_soup):
        courses = list()
        course_table = semester_soup.find("table", attrs={'class': "tablesorter"})

        if course_table:
            table_body = course_table.find("tbody")
            for row in table_body.find_all("tr"):
                content = row.find_all('td')
                course_name = content[1].text
                course_link = WebsiteClient.BASE_URL + content[1].find('a')['href']
                course_lecturer = content[2].text.strip()
                course = Course(course_name, course_link, course_lecturer)
                self.add_events_to_course(course)
                courses.append(course)
        return courses

    def add_events_to_course(self, course):
        soup = self.get_page_soup(course.course_link)
        reiter_tab = soup.find('ul', attrs={'class': 'reiter'})

        if reiter_tab:
            # does not exist for old list. E.g. WS 2017 HR, Lisgens
            reiter_tab_lis = reiter_tab.find_all('li')
            reiter_tab_li = reiter_tab_lis[1]
            link_to_courses = WebsiteClient.BASE_URL + reiter_tab_li.find('a')['href']

            soup2 = self.get_page_soup(link_to_courses)
            course_list_element = soup2.find('ul', attrs={'id': 'allererste'})

            if course_list_element is not None:
                for event_element in course_list_element.findChildren('li', recursive=False):

                    course_name = self.get_event_title(event_element)
                    if course_name is not None:

                        event = Event(course_name)
                        self.add_material_to_event(event, event_element)
                        # check config "show all events" here and add as a condition to if statement
                        if event.material_list:
                            course.event_list.append(event)
        return

    def get_event_title(self, event_element):
        title_variant_a = event_element.find('span', attrs={'class': 'title'})
        title_variant_b = event_element.find('div', attrs={'class': 'head'})

        if title_variant_a:
            return title_variant_a.text
        elif title_variant_b:
            return title_variant_b.text
        else:
            return None

    def add_material_to_event(self, event, event_element):
        material_list = event_element.find('ul')
        for material_element in material_list:
            title = None
            download_url = None
            file_name = None
            uploaded_date = self.get_uploaded_date(material_element)

            title_element = material_element.find('div', attrs={'class': 'title1'})
            if title_element is not None:
                title = title_element.text

            toolbar_element = material_element.find('div', attrs={'class': 'toolbar'})

            if toolbar_element is not None:
                download_element = toolbar_element.find('a')
                if download_element is not None:
                    download_url = download_element['href']

            # Todo: schöner machen. Wenn elment kein filecontent hat nach filedownload suchen.
            file_content_element = material_element.find('div', attrs={'class': 'filecontent'})
            if file_content_element is None:
                file_content_element = material_element.find('div', attrs={'class': 'filedownload'})

            if file_content_element is not None:
                download_element = file_content_element.find('a')
                if download_element is not None:
                    full_download_path = download_element['href']

                    file_name = re.search(r'([^/]*)$', full_download_path).group()

            if title is not None and download_url is not None:
                event.material_list.append(
                    Material(
                        title,
                        WebsiteClient.DOWNLOAD_BASE_URL + download_url,
                        uploaded_date,
                        file_name
                    ))
        return None

    def get_uploaded_date(self, html_element):
        uploaded_date = None
        try:
            title_element = html_element.find('div', attrs={'class': 'title2'})
            title_text = title_element.find('span', attrs={'class': 'text'}).text

            uploaded_date = title_text.split(',')[1]
            uploaded_date = uploaded_date.strip()

        except Exception as error:
            self.logger.log(error)
        return uploaded_date
