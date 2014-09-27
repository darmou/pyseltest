# Copyright 2014 Andrew Magee.
# Distributed under the GPL v3 licence: http://www.gnu.org/licenses/gpl-3.0.html

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

class MyTestDriver:
    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url

    def open_page(self, path):
        return self.browser.get(self.base_url + path)

    def get_element(self, css=None, model=None, text=None):
        list = self.get_elements(css=css, model=model, text=text)
        if list == []:
            raise Exception("Not found")
        if len(list) > 1:
            raise Exception("Too many")
        return list[0]

    def get_elements(self, css=None, model=None, text=None):
        """
        d.get_elements(css="a", text="hello")
        >>> List of <a> tags whose text exactly equals "hello"
        """
        if not any((css, model, text)):
            raise ValueError()
        sets = []
        if text is not None:
            sets.append(set([e for e in self.get_elements(css="*") if e.text == text]))
        if css is not None:
            sets.append(set(self.browser.find_elements_by_css_selector(css)))
        if model is not None:
            sets.append(set(self.get_elements(css="[ng-model='{}']".format(model))))
        return list(set.intersection(*sets))

    def element_exists(self, **kwargs):
        return self.get_elements(**kwargs) != []

    def wait_until(self, func, timeout=2):
        WebDriverWait(self.browser, timeout).until(func)

    def wait_for_element(self, css=None, model=None, timeout=2):
        self.wait_until(lambda br: self.get_elements(css=css, model=model) != [], timeout)


# Monkeypatch WebElement with some useful methods.

@property
def left(self):
    return self.location['x']

@property
def top(self):
    return self.location['y']

@property
def width(self):
    return self.size['width']

@property
def height(self):
    return self.size['height']

@property
def right(self):
    return self.left + self.width

@property
def bottom(self):
    return self.top + self.height

WebElement.left = left
WebElement.top = top
WebElement.width = width
WebElement.height = height
WebElement.right = right
WebElement.bottom = bottom


