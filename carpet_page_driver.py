import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.carpetright.co.uk/carpets/'
driver = webdriver.Chrome()  # Use webdriver.Firefox() for Firefox

driver.get(url)

# Accept cookie consent
try:
    cookie_consent_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@class="coi-consent-banner__agree-button"]'))
    )
    cookie_consent_button.click()
    print("Cookies Accepted")
except:
    print("Failed to locate or click the cookie consent button.")

# Keep clicking the "load more" button until it's no longer available
while True:
    try:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button._1ONC9J._2FpaaR'))
        )
        load_more_button.click()
        print("Load more clicked")
        time.sleep(2)  # Adjust the sleep time if needed
    except:
        break

# Cache resonse 
html_file_name = 'carpets_page.html'

with open(html_file_name, 'w', encoding='utf-8') as html_file:
    html_file.write(driver.page_source)

print(f"HTML content saved to {html_file_name}")

##############
