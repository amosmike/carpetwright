import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

html_file_name = 'carpets_page.html'

with open(html_file_name, 'r', encoding='utf-8') as html_file:
    soup = BeautifulSoup(html_file.read(), 'html.parser')

# Extract the required data
product_data_list = []
product_list = soup.find_all('div', {'class': '_2AQ0-F'})

for product in product_list:
    product_data = {}
    
    product_name = product.find('p', {'class': '_3YYg4o'})
    product_data['name'] = product_name.text.strip() if product_name else 'null'

    product_sale_price = product.find('p', {'class': '_3ofUnR'})
    product_data['sale_price'] = product_sale_price.find('span').text.strip() if product_sale_price else 'null'

    product_price = product.find('p', {'class': '_1qo80M'})
    product_data['price'] = product_price.find('span').text.strip() if product_price else 'null'

    product_prev_price = product.find('p', {'class': '_3P3gPg'})
    product_data['previous_price'] = product_prev_price.find('span').text.strip() if product_prev_price else 'null'

    product_data_list.append(product_data)

# Export the data to a CSV file
csv_file_name = 'product_data.csv'
csv_columns = ['name', 'price', 'sale_price', 'previous_price']

with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for product_data in product_data_list:
        writer.writerow(product_data)

print(f"Data exported to {csv_file_name}")
