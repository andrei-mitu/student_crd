import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import service.web.webdriver as webdriver
from model.models import Note, Course

USM_LINK = 'http://studentcrd.usm.md/Default.aspx'
LABEL_XPATH = '/html/body/div/div[3]/form/p[1]/input'
SUBMIT_XPATH = '/html/body/div/div[3]/form/p[2]/input'
NOTES_TAB_XPATH = '/html/body/div/form/nav/div/a[3]'


def fetch_data(driver, semester=None):
    courses = []
    time.sleep(2)
    semester = semester if semester is not None and semester != 'Skip' else 'last()'
    object_xpath = f"/html/body/div/form/div[4]/div[3]/div/table[{semester}]/tbody/tr/td[1]/b"
    note_xpath = f"/html/body/div/form/div[4]/div[3]/div/table[{semester}]/tbody/tr/td[contains(@style,'color:green')]"

    for course in driver.find_elements(By.XPATH, object_xpath):
        if course.text == '':
            continue
        notes = []
        iterator = 0
        for element in driver.find_elements(By.XPATH, note_xpath):
            if element.text == '' or iterator == 3:
                continue
            if element.find_element(By.XPATH, "../preceding-sibling::tr/td[1]/b").text == course.text:
                notes.append(Note(element.text, element.find_element(By.XPATH, '../td[2]/i').text))
                iterator += 1
        courses.append(Course(course.text, notes))
    return courses


def get(idnp, semester=None) -> list[Course]:
    driver = webdriver.new_driver()
    driver.get(USM_LINK)
    driver.find_element(By.XPATH, LABEL_XPATH).send_keys(idnp)
    driver.find_element(By.XPATH, SUBMIT_XPATH).click()
    element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(driver.find_element(By.XPATH, NOTES_TAB_XPATH)))
    element.click()

    courses = fetch_data(driver, semester)
    driver.quit()
    return courses
