import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--window-size=1920,1080")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def pytest_addoption(parser):
    parser.addoption("--state", action="store", default="Uttar Pradesh", help="State to scrape")
    parser.addoption("--constituency", action="store", default="Mirzapur", help="Constituency to scrape")

@pytest.fixture
def state_visible_text(request):
    return request.config.getoption("--state")

@pytest.fixture
def constituency_name(request):
    return request.config.getoption("--constituency")
