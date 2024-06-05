import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption("--state", action="store", help="State visible text")
    parser.addoption("--constituency", action="store", help="Constituency name")


@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()


@pytest.fixture
def state_visible_text(request):
    return request.config.getoption("--state")


@pytest.fixture
def constituency_name(request):
    return request.config.getoption("--constituency")
