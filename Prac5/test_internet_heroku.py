from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


BASE_URL = "https://www.saucedemo.com/"
WAIT_SECONDS = 10
DEMO_DELAY_SECONDS = 3


def pause_between_steps() -> None:
    """Pause so each browser action is visible during a demonstration."""
    sleep(DEMO_DELAY_SECONDS)


def test_night_shift_shopping_journey() -> None:
    """Buy the cheapest item and verify the order confirmation."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, WAIT_SECONDS)

    try:
        driver.get(BASE_URL)
        pause_between_steps()

        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        pause_between_steps()
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        pause_between_steps()
        driver.find_element(By.ID, "login-button").click()
        pause_between_steps()

        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title")))
        assert driver.find_element(By.CLASS_NAME, "title").text == "Products"
        pause_between_steps()

        Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_value("lohi")
        pause_between_steps()
        products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item")))
        cheapest_product = products[0]
        cheapest_name = cheapest_product.find_element(By.CLASS_NAME, "inventory_item_name").text
        add_to_cart_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".inventory_item button")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart_button)
        driver.execute_script("arguments[0].click();", add_to_cart_button)
        pause_between_steps()

        cart_badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        assert cart_badge.text == "1"
        cart_link = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link")))
        driver.execute_script("arguments[0].click();", cart_link)
        wait.until(EC.url_contains("cart.html"))
        pause_between_steps()

        cart_item = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cart_item")))
        assert cart_item.find_element(By.CLASS_NAME, "inventory_item_name").text == cheapest_name
        pause_between_steps()
        checkout_button = wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkout_button)
        driver.execute_script("arguments[0].click();", checkout_button)
        wait.until(EC.url_contains("checkout-step-one.html"))
        pause_between_steps()

        wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Vruxak")
        pause_between_steps()
        driver.find_element(By.ID, "last-name").send_keys("Patel")
        pause_between_steps()
        driver.find_element(By.ID, "postal-code").send_keys("380009")
        pause_between_steps()
        continue_button = wait.until(EC.element_to_be_clickable((By.ID, "continue")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_button)
        driver.execute_script("arguments[0].click();", continue_button)
        wait.until(EC.url_contains("checkout-step-two.html"))
        pause_between_steps()
        finish_button = wait.until(EC.element_to_be_clickable((By.ID, "finish")))
        driver.execute_script("arguments[0].click();", finish_button)
        pause_between_steps()

        confirmation = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "complete-header")))
        assert confirmation.text == "Thank you for your order!"
        print(f"PASS: ordered the cheapest product ({cheapest_name})")

    except (AssertionError, WebDriverException):
        screenshot = Path(__file__).with_name("test4_failure.png")
        driver.save_screenshot(str(screenshot))
        raise
    finally:
        driver.quit()


if __name__ == "__main__":
    test_night_shift_shopping_journey()

# From PowerShell in Prac5:
# py -m venv .venv
# .\.venv\Scripts\python.exe -m pip install -r requirements.txt
# .\.venv\Scripts\python.exe test_internet_heroku.py
# Requires Google Chrome and internet access to SauceDemo. Selenium Manager may also
# need internet access to obtain a compatible ChromeDriver if one is not available.
