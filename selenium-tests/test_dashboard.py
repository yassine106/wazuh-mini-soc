import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

USERNAME = os.getenv("TEST_USER")
PASSWORD = os.getenv("TEST_PASS")

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")  # <-- ignore self-signed SSL
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_dashboard_reachable(driver):
    driver.get("https://3.92.21.45")
    sleep(2)
    WebDriverWait(driver, 10).until(lambda d: "Wazuh" in d.title)
    assert "Wazuh" in driver.title

def test_login_form_present(driver):
    driver.get("https://3.92.21.45/app/login")
    user_field = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-subj="user-name"]'))
    )
    pass_field = driver.find_element(By.CSS_SELECTOR, '[data-test-subj="password"]')
    login_button = driver.find_element(By.CSS_SELECTOR, '[data-test-subj="submit"]')
    assert user_field and pass_field and login_button
    

def test_login_success(driver):
    driver.get("https://3.92.21.45/app/login")
    WebDriverWait(driver, 15).until(
         EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test-subj="user-name"]'))
     )
    
    driver.find_element(By.CSS_SELECTOR, '[data-test-subj="user-name"]').send_keys(USERNAME)
    driver.find_element(By.CSS_SELECTOR, '[data-test-subj="password"]').send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, '[data-test-subj="submit"]').click()
    # Example: check sidebar element exists after login
    sidebar = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH,
    '//span[text()="Agents summary"]'))
    )
    assert sidebar
