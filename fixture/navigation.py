#  __author__ = 'Alexey Buchkin'


class NavigationHelper:

    def __init__(self, app, base_url):
        self.app = app
        self.base_url = base_url

    def open_home_page(self):
        wd = self.app.wd
        # open home page
        wd.get(self.base_url)
