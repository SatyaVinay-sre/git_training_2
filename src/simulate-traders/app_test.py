import random
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException, TimeoutException

url = os.getenv("URL")

# List of stocks to choose from
stocks = ["AAPL", "NFLX", "QQQ", "SPY", "GLD"]

# Login credentials for both users
user_credentials = {
    "user1": {"username": "admin", "password": "admin"},
    "user2": {"username": "wiley", "password": "wiley"}
}

# Number of iterations to run
num_iterations = 10

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')
    return webdriver.Chrome(options=chrome_options)

def login(driver, username, password):
    driver.get(f"https://{url}/login")
    wait = WebDriverWait(driver, 10)
    username_field = wait.until(EC.presence_of_element_located((By.ID, "uname")))
    password_field = driver.find_element(By.ID, "password")
    
    # Enter login credentials
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

def perform_order(driver, wait, stock, user_id):
    try:
        # Wait for the "Quotes" link to appear and navigate to it
        quotes_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Quotes")))

        print(f"User {user_id}: Placing order for {stock}")

        # Navigate to the Quotes page
        quotes_link.click()

        # Type the chosen stock into the search input field
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "search")))
        search_input.clear()
        search_input.send_keys(stock)
        search_input.send_keys(Keys.RETURN)  # Ensure the search is submitted

        # Wait until the "buy" link for the stock appears and click it
        buy_link = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//a[@class='Order_buy__BEVBq' and contains(@href, '/Trade/buy/{stock}')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", buy_link)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//a[@class='Order_buy__BEVBq' and contains(@href, '/Trade/buy/{stock}')]")))
        driver.execute_script("arguments[0].click();", buy_link)

        # Wait for the quantity input field and increment button to be visible
        quantity_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[role='spinbutton']"))
        )
        decrement_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Decrement value']"))
        )
        increment_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Increment value']"))
        )

        # Choose a random quantity between 1 and 10
        random_quantity = random.randint(1, 10)
        print(f"User {user_id}: Setting quantity to {random_quantity}")

        # Choose randomly between incrementing or decrementing
        if random.choice([True, False]):
            print(f"User {user_id}: Placing buy order")
            # Increment to the random quantity
            current_quantity = int(quantity_input.get_attribute("value"))
            while current_quantity < random_quantity:
                increment_button.click()
                current_quantity += 1
        else:
            print(f"User {user_id}: Placing sell order")
            # Decrement to the random quantity
            current_quantity = int(quantity_input.get_attribute("value"))
            while current_quantity > random_quantity * -1:
                decrement_button.click()
                current_quantity -= 1

        # Click the "Place Order" button
        place_order_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.OrderList_lgBtn__vVG2q"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", place_order_button)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.OrderList_lgBtn__vVG2q")))
        driver.execute_script("arguments[0].click();", place_order_button)

        print(f"User {user_id}: Order placed for {stock}")

        # Handle alert if present
        try:
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert.accept()  # Or use alert.dismiss() to dismiss the alert
            print(f"User {user_id}: Alert handled.")
        except Exception as inner_e:
            print(f"User {user_id}: Failed to handle alert: {inner_e}")

    except (UnexpectedAlertPresentException, NoSuchElementException, TimeoutException) as e:
        # Handle specific exceptions and retry
        print(f"User {user_id}: Error encountered: {e}. Retrying...")
        # Optionally refresh the quotes page
        driver.get("https://{url}/quotes")
        return False  # Indicate retry is needed

    except Exception as e:
        # Handle any other exceptions
        print(f"User {user_id}: Unexpected error encountered: {e}")
        driver.get("https://{url}/quotes")
        return False  # Indicate retry is needed

    return True  # Indicate success

def main():
    driver1 = setup_driver()
    driver2 = setup_driver()

    try:
        # Log in both users
        login(driver1, user_credentials["user1"]["username"], user_credentials["user1"]["password"])
        login(driver2, user_credentials["user2"]["username"], user_credentials["user2"]["password"])

        # Run for a fixed number of iterations
        for _ in range(num_iterations):
            # Perform orders in alternating sessions
            for driver, user_id in [(driver1, 1), (driver2, 2)]:
                stock = random.choice(stocks)
                if not perform_order(driver, WebDriverWait(driver, 10), stock, user_id):
                    continue  # Retry if needed

                # Wait for 10 seconds before the next iteration
                time.sleep(10)

    finally:
        # Clean up by closing the browsers
        driver1.quit()
        driver2.quit()

if __name__ == "__main__":
    main()
