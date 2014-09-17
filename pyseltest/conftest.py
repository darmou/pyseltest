import os
import pytest
from pyseltest.helpers import MyTestDriver


def pytest_addoption(parser):
    parser.addoption("--browser",
        action="store",
        default="firefox"
    )
    parser.addoption("--xvfb",
        action="store_true",
        default=False,
    )


@pytest.yield_fixture(scope='session')
def app():
    from app import create_app
    a = create_app("config.TestingConfig")
    with a.app_context():
        a.drop_all()
        a.init_db()
        a.connection = a.engine.connect()
        a.db_session.configure(bind=a.connection)
        yield a
        a.connection.close()


@pytest.yield_fixture(scope="function")
def session(app):
    """
    Creates a new database session (with working transaction)
    for a test duration.
    """
    app.transaction = app.connection.begin()

    # pushing new Flask application context for multiple-thread
    # tests to work
    ctx = app.app_context()
    ctx.push()

    session = app.db_session()

    yield session

    # the code after yield statement works as a teardown
    app.transaction.close()
    session.close()
    ctx.pop()


@pytest.yield_fixture
def xvfb(request):
    from xvfbwrapper import Xvfb

    vdisplay = Xvfb()
    vdisplay.start()

    yield

    vdisplay.stop()


@pytest.yield_fixture
def pass_through(request):
    yield


@pytest.yield_fixture
def browser(request):
    """
    http://chromedriver.storage.googleapis.com/index.html
    """

    if request.config.getoption("--xvfb"):
        f = xvfb
    else:
        f = pass_through

    from contextlib import contextmanager
    with contextmanager(f)(request):
        from selenium import webdriver
        browser_name = request.config.getoption("--browser")
        if browser_name == "firefox":
            browser = webdriver.Firefox()
        elif browser_name == "phantomjs":
            browser = webdriver.PhantomJS()
        elif browser_name == "chrome":
            browser = webdriver.Chrome("./chromedriver")
        else:
            raise Exception("Invalid browser name")
        yield browser
        browser.quit()


@pytest.yield_fixture
def driver(browser):
    import config
    yield MyTestDriver(
        browser=browser, 
        base_url="http://" + config.TestingConfig.SERVER_NAME
    )


@pytest.yield_fixture
def xvfb_browser(xvfb, browser):
    yield browser


@pytest.yield_fixture
def test_client(app):
    yield app.test_client()
