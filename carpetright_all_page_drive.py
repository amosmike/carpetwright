import re
import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# List of URLs
urls = [
    'https://www.carpetright.co.uk/carpets/',
    'https://www.carpetright.co.uk/beds/',
    'https://www.carpetright.co.uk/mattresses/',
    'https://www.carpetright.co.uk/engineered-wood/',
    'https://www.carpetright.co.uk/laminate/',
    'https://www.carpetright.co.uk/rugs/',
    'https://www.carpetright.co.uk/underlay/'
]

driver = webdriver.Chrome()  # Use webdriver.Firefox() for Firefox

product_data_list = []

for url in urls:
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

    # Save the HTML content to a local file
    html_file_name = f"{url.split('/')[-2]}.html"
    with open(html_file_name, 'w', encoding='utf-8') as html_file:
        html_file.write(driver.page_source)

    print(f"HTML content saved to {html_file_name}")

    # Parse the content with Beautiful Soup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract the required data
    product_list = soup.find_all('div', {'class': '_2AQ0-F'})

    for product in product_list:
        product_data = {}

        product_data['category'] = f"{url.split('/')[-2]}"

        product_name = product.find('p', {'class': '_3YYg4o'})
        product_data['name'] = product_name.text.strip() if product_name else 'null'

        product_sale_price = product.find('p', {'class': '_3ofUnR'})
        product_data['sale_price'] = product_sale_price.find('span').text.strip() if product_sale_price else 'null'

        product_price = product.find('p', {'class': '_1qo80M'})
        product_data['normal_price'] = product_price.find('span').text.strip() if product_price else 'null'

        product_prev_price = product.find('p', {'class': '_3P3gPg'})
        product_data['previous_price'] = product_prev_price.find('span').text.strip() if product_prev_price else 'null'

        product_data_list.append(product_data)

driver.quit()

# Export the data to a CSV file
csv_file_name = "carpetwright_product_data.csv"
csv_columns = ['category', 'name', 'normal_price', 'sale_price', 'previous_price']

with open(csv_file_name, mode='w', newline='', encoding='utf8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()
    for product_data in product_data_list:
        writer.writerow(product_data)

print(f"Product data exported to {csv_file_name}")
