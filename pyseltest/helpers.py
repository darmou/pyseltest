# Copyright 2014 Andrew Magee.
# Distributed under the GPL v3 licence: http://www.gnu.org/licenses/gpl-3.0.html

from selenium.webdriver.support.ui import WebDriverWait

class MyTestDriver:
    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url

    def open_page(self, path):
        return self.browser.get(self.base_url + path)

    def get_element(self, css=None, model=None):
        list = self.get_elements(css=css, model=model)
        if list == []:
            raise Exception("Not found")
        if len(list) > 1:
            raise Exception("Too many")
        return list[0]

    def get_elements(self, css=None, model=None, text=None):
        if css is not None:
            return self.browser.find_elements_by_css_selector(css)
        elif model is not None:
            return self.get_elements(css="[ng-model='{}']".format(model))
        elif text is not None:
            return [e for e in self.get_elements(css="*") if e.text == text]
        else:
            raise ValueError()

    def element_exists(self, **kwargs):
        return self.get_elements(**kwargs) != []

    def wait_until(self, func, timeout=2):
        WebDriverWait(self.browser, timeout).until(func)

    def wait_for_element(self, css=None, model=None, timeout=2):
        self.wait_until(lambda br: self.get_elements(css=css, model=model) != [], timeout)





