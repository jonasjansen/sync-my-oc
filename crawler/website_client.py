import requests
from gui.login_dialog import LoginDialog


class WebsiteClient:
    BASE_URL = "https://campus.bildungscentrum.de"
    LOGIN_POST_URL = "/nfcampus/Login.do"
    DOWNLOAD_BASE_URL = "https://campus.bildungscentrum.de/nfcampus/"

    login_dialog = None
    login_session = None
    start_page_url = None
    logger = None

    def __init__(self, logger):
        self.login_dialog = LoginDialog()
        self.logger = logger
        return

    def get_start_page_url(self):
        if self.start_page_url is None:
            self.login()
        return self.start_page_url

    def get_login_session(self):
        if self.login_session is None:
            self.login()
        return self.login_session

    def login(self):
        post_data = self.get_login_data()
        login_session = requests.session()
        login_url = self.BASE_URL + self.LOGIN_POST_URL
        result = login_session.post(
            self.BASE_URL + self.LOGIN_POST_URL,
            post_data
        )
        if result.url == login_url:
            self.login_dialog = LoginDialog()
            raise Exception("Login Daten waren nicht korrekt")
        if result.status_code == 200 and not result.url == login_url:
            self.logger.log('Login successful:', result.status_code, result.reason)
            self.login_session = login_session
            self.start_page_url = result.url

    def get_login_data(self):

        result = dict()

        while not self.login_dialog.has_login_data:
            self.login_dialog.show()
            self.login_dialog.exec()

            if self.login_dialog.was_canceled:
                raise Exception("Keine Logindaten eingeben!")

            result['name'] = self.login_dialog.usernameInput.text()
            result['password'] = self.login_dialog.passwordInput.text()
        return result

