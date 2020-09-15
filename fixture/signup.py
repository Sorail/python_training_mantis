import re
import quopri


class SignupHelper:

    def __init__(self, app):
        self.app = app

    def new_user(self, username, email, password):
        wd = self.app.wd
        wd.get(self.app.config['web']['baseUrl'] + "/signup_page.php")
        wd.find_element_by_name("username").click()
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("email").click()
        wd.find_element_by_name("email").clear()
        wd.find_element_by_name("email").send_keys(email)
        wd.find_element_by_xpath("//input[@type='submit']").click()

        mail = self.app.mail.get_mail(username, password, '[MantisBT] Account registration')
        url = self.extract_confirmation_url(mail)

        wd.get(url)

        wd.find_element_by_name("realname").click()
        wd.find_element_by_name("realname").clear()
        wd.find_element_by_name("realname").send_keys(username)
        wd.find_element_by_name("password").click()
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_name("password_confirm").click()
        wd.find_element_by_name("password_confirm").clear()
        wd.find_element_by_name("password_confirm").send_keys(password)
        wd.find_element_by_xpath("//button[@type='submit']").click()

    def extract_confirmation_url(self, text):
        body = quopri.decodestring(text).decode('utf-8')
        return re.search("http://.*", body).group(0)
