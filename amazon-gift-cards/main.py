import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

DEV = True

# Entries are in the format of "NAME": ("DIGITS", RUN_COUNT)
cards = { 
    "NAME": ("DIGITS", 2)
}

# Minimum is $1, should be a number (int or float)
PURCHASE_AMOUNT = 1

EDGE_BINARY_LOCATION = ""
EDGE_USER_DATA_DIR = ""
EDGE_BETA_LOCAL_STORE = ""

AMAZON_PURCHASE_LINK = "https://www.amazon.com/gp/product/B086KKT3RX?ref_=gcui_b_e_rb_c_d"

# Init WebDriver
service = webdriver.EdgeService(executable_path="./msedgedriver.exe")
options = webdriver.EdgeOptions()
options.add_argument(f"user-data-dir={EDGE_USER_DATA_DIR}")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.binary_location= EDGE_BINARY_LOCATION

driver = webdriver.Edge(options=options, service=service)

for card, detail in cards.items():
    digits, runs = detail

    print(f"--------- {card} ---------")
    for i in range(runs):
        print(f"Purchase {i + 1} of {runs}")

        # Navigate to purchase link
        driver.get(AMAZON_PURCHASE_LINK)

        # Fill in $1 reload + purchase
        reload_amount_field = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@name='oneTimeReloadAmount']")))
        reload_amount_field.send_keys(str(PURCHASE_AMOUNT))

        purchase_button = driver.find_element(By.XPATH, "//div[@id='buyNow_feature_div']")
        purchase_button.click()

        # NOTE Redirects

        # Change payment method
        change_payment_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@id='payChangeButtonId']")))
        change_payment_button.click()

        # Click on desired card
        try:
            card_digit_text = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f"//span[contains(text(), 'ending in {digits}')]")))
        except TimeoutException:
            print(f"{card} not found in payment methods")
            break

        webdriver.ActionChains(driver).move_to_element(card_digit_text).click(card_digit_text).perform()

        # May need to add a wait if card number needs to be confirmed

        # Set desired card as payment
        use_payment_button = driver.find_element(By.XPATH, "//span[@id='orderSummaryPrimaryActionBtn']")
        use_payment_button.click()

        # NOTE Redirects

        # Submit payment
        if not DEV:
            place_order_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@id='submitOrderButtonId']")))
            place_order_button.click()

        driver.implicitly_wait(2)

    print()

driver.close()