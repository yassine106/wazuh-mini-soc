import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

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
    WebDriverWait(driver, 10).until(
    assert "Wazuh" in driver.title)

def test_login_form_present(driver):
    driver.get("https://3.92.21.45/app/login")
    user_field = driver.find_element(By.CSS_SELECTOR, '[data-test-subj="user-name"]')
    pass_field = driver.find_element(By.CSS_SELECTOR, '[data-test-subj="password"]')
    login_button = driver.find_element(By.CSS_SELECTOR, '[data-test-subj="submit"]')
    assert user_field and pass_field and login_button

def test_login_success(driver):
    driver.get("https://<your-wazuh-dashboard-host>/login")
    driver.find_element(By.CSS_SELECTOR, '[data-test-subj="user-name"]').send_keys("${{ secrets.WAZUH_TEST_USER }}")
    driver.find_element(By.CSS_SELECTOR, '[data-test-subj="password"]').send_keys("${{ secrets.WAZUH_TEST_PASS }}")
    driver.find_element(By.CSS_SELECTOR, '[data-test-subj="submit"]').click()
    # Example: check sidebar element exists after login
    assert driver.find_element(By.ID, "sidebar")
