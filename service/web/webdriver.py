import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def chrome_options() -> Options:
    options = Options()
    options.headless = True
    options.page_load_strategy = 'normal'
    return options


def service() -> Service:
    return Service(os.environ.get('WEB_DRIVER_LOCATION'))


def new_driver() -> webdriver.Chrome:
    load_dotenv()
    return webdriver.Chrome(service=service(), options=chrome_options())
