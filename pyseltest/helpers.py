# Copyright 2014 Andrew Magee.
# Distributed under the GPL v3 licence: http://www.gnu.org/licenses/gpl-3.0.html

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from ordered_set import OrderedSet
import inspect
import re


class ElementMethods:
    """
    This class is just a holder for methods that will be used both on the
    `MyTestDriver` class and also monkey-patched onto the Selenium `WebElement`
    class.
    """

    def __init__(self):
        raise ValueError("Don't try to create an ElementMethods object.")

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

        # Use ordered sets so we don't muck up the ordering if the caller
        # specifies two or more arguments.
        items = None
        def update(new_items):
            nonlocal items
            if items == None:
                items = OrderedSet(new_items)
            else:
                items = items & OrderedSet(new_items)

        if text is not None:
            update([e for e in self.get_elements(css="*") if e.text == text])
        if css is not None:
            update(self._get_element().find_elements_by_css_selector(css))
        if model is not None:
            update(self.get_elements(css="[ng-model='{}']".format(model)))
        return items

    def element_exists(self, **kwargs):
        return self.get_elements(**kwargs) != []

    def get_classes(self):
        return [c for c in re.split(r'\s+', self.get_attribute("class")) if c]


class MyTestDriver:
    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url

    def open_page(self, path):
        return self.browser.get(self.base_url + path)

    def wait_until(self, func, timeout=2):
        WebDriverWait(self.browser, timeout).until(func)

    def wait_for_element(self, css=None, model=None, timeout=2):
        self.wait_until(lambda br: self.get_elements(css=css, model=model) != [], timeout)

    def _get_element(self):
        """
        For the ElementMethods methods.
        """
        return self.browser


"""
Make the methods in ElementMethods callable from MyTestDriver objects and
WebElement objects.
"""
for n, f in inspect.getmembers(ElementMethods, predicate=inspect.isfunction):
    if n != "__init__":
        setattr(MyTestDriver, n, f)
        setattr(WebElement, n, f)


"""
For the ElementMethods methods.
"""
def _webelement_get_element(self):
    return self
WebElement._get_element = _webelement_get_element



"""
Monkey-patch WebElement with some other useful methods.
"""

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


