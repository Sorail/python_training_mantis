#  __author__ = 'Alexey Buchkin'
from selenium import webdriver
from fixture.session import SessionHelper
from fixture.navigation import NavigationHelper
from fixture.project import ProjectHelper


class Application:

    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "IE":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser: %s", browser)
        self.wd.implicitly_wait(1)
        self.navigation = NavigationHelper(self, base_url)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)

    def is_valid(self):
        try:
            self.wd.current_url()
            return True
        except:
            return False

    def destroy(self):
        self.wd.quit()