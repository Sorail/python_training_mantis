#  __author__ = 'Alexey Buchkin'

from selenium.webdriver.support.ui import Select
from time import sleep


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    project_cache = None

    def open_project_page(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//span[text()=' Управление ']").click()
        wd.find_element_by_xpath("//a[text()='Управление проектами']").click()

    def create(self, project):
        wd = self.app.wd
        wd.find_element_by_xpath("//button[text()='Создать новый проект']").click()
        self.fill_form(project)

    def fill_form(self, project):
        wd = self.app.wd
        self.change_field("name", project.name)
        self.change_field("status", project.status)
        self.change_field("inherit_global", project.inherit_global)
        self.change_field("view_state", project.view_state)
        self.change_field("description", project.description)
        wd.find_element_by_xpath("//input[@value='Добавить проект']").click()

    def change_field(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            if "status" in field_name:
                wd.find_element_by_xpath("//select[@name='%s']" % field_name).click()
                Select(wd.find_element_by_name(field_name)).select_by_visible_text("%s" % text)
                wd.find_element_by_xpath("//select[@name='%s']//option[text()='%s']" % (field_name, text)).click()
            elif "inherit_global" in field_name:
                status = wd.find_element_by_xpath("//input[@name='inherit_global']").get_attribute("checked")
                pram = str(text).lower()
                if status != pram:
                    wd.find_element_by_xpath("//input[@name='inherit_global']/..").click()
            elif "view_state" in field_name:
                wd.find_element_by_name(field_name).click()
                Select(wd.find_element_by_name(field_name)).select_by_visible_text("%s" % text)
                wd.find_element_by_xpath("//select[@name='%s']//option[text()='%s']" % (field_name, text)).click()
            else:
                wd.find_element_by_name(field_name).click()
                wd.find_element_by_name(field_name).clear()
                wd.find_element_by_name(field_name).send_keys(text)
