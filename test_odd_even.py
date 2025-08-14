import time
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://localhost"
HEALTH_URL = f"{BASE_URL}/api/health"
TIMEOUT = 20


def wait_for_server():
    """בדיקה שהשרת זמין לפני הרצת הבדיקה."""
    start = time.time()
    while time.time() - start < TIMEOUT:
        try:
            r = requests.get(HEALTH_URL, timeout=3)
            if r.ok and r.json().get("ok"):
                return
        except:
            pass
        time.sleep(1)
    raise RuntimeError("Server is not ready")


def new_driver():
    chrome_options = Options()
    for opt in [
        "--headless=new",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage",
    ]:
        chrome_options.add_argument(opt)
    return webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options
    )


def get_message(driver):
    msg = driver.find_element(By.ID, "message")
    return msg.text.strip(), (msg.get_attribute("class") or "").strip()


def test_odd_even():
    wait_for_server()
    driver = new_driver()
    wait = WebDriverWait(driver, 10)

    try:
        # פתיחת הדף הראשי
        driver.get(BASE_URL)

        # איתור רכיבים
        number_input = wait.until(EC.presence_of_element_located((By.ID, "numberInput")))
        check_btn = wait.until(EC.element_to_be_clickable((By.ID, "checkBtn")))
        clear_btn = wait.until(EC.element_to_be_clickable((By.ID, "clearBtn")))

        # תרחיש 1: קלט ריק
        check_btn.click()
        wait.until(lambda d: get_message(d)[0] != "")
        text, cls = get_message(driver)
        assert "Please enter a number" in text and cls == "error"

        # תרחיש 2: מספר עשרוני
        number_input.send_keys("2.5")
        check_btn.click()
        wait.until(lambda d: "integer" in get_message(d)[0])
        text, cls = get_message(driver)
        assert "integer" in text and cls == "error"

        # ניקוי
        clear_btn.click()
        assert number_input.get_attribute("value") == ""
        assert get_message(driver)[0] == ""

        # תרחיש 3: מספר זוגי
        number_input.send_keys("8")
        check_btn.click()
        wait.until(lambda d: "Result: Even" in get_message(d)[0])
        text, cls = get_message(driver)
        assert "Result: Even" in text and cls == "even"

        # תרחיש 4: מספר אי זוגי
        number_input.send_keys(Keys.CONTROL, "a")
        number_input.send_keys(Keys.DELETE)
        number_input.send_keys("7")
        check_btn.click()
        wait.until(lambda d: "Result: Odd" in get_message(d)[0])
        text, cls = get_message(driver)
        assert "Result: Odd" in text and cls == "odd"

    finally:
        driver.quit()


if __name__ == "__main__":
    test_odd_even()
