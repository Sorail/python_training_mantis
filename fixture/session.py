#  __author__ = 'Alexey Buchkin'
import time


class SessionHelper:

    def __init__(self, app):
        self.app = app

    def login(self, username, password):
        wd = self.app.wd
        self.app.navigation.open_home_page()
        # login
        wd.find_element_by_name("username").click()
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_xpath("//input[@type='submit']").click()
        wd.find_element_by_name("password").click()
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_xpath("//input[@type='submit']").click()

    def ensure_login(self, username, password):
        wd = self.app.wd
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:
                self.logout()
        self.login(username, password)

    def logout(self):
        wd = self.app.wd
        # logout
        wd.find_element_by_xpath("//span[@class='user-info']").click()
        wd.find_element_by_xpath("//a[text()=' Logout']").click()
        wd.find_element_by_name("username")

    def ensure_logout(self):
        wd = self.app.wd
        # logout
        if self.is_logged_in():
            time.sleep(1)
            wd.find_element_by_xpath("//span[@class='user-info']").click()
            wd.find_element_by_xpath("//a[text()=' Logout']").click()
            wd.find_element_by_name("username")

    def is_logged_in(self):
        wd = self.app.wd
        return len(wd.find_elements_by_xpath("//span[@class='user-info']")) > 0

    def is_logged_in_as(self, username):
        return self.get_logged_user() == username

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_xpath("//span[@class='user-info']").text
