from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

#Starts the driver and goes to our starting webpage
driver = webdriver.Chrome() #'C:/Web Scraping course/chromedriver.exe')

driver.get('https://www.nike.com/ca/w/sale-3yaep')

#Will keep scrolling down the webpage until it cannot scroll no more
last_height = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(3)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height

#Imports the HTML of the webpage into python  
soup = BeautifulSoup(driver.page_source, 'html.parser')

#grabs the HTML of each product
product_card = soup.find_all('div', class_ = 'product-card__body')

#Creates a dataframe
product_dict = {'Link':[''], 'Name':[''], 'Subtitle':[''], 'Price':[''], 'Sale Price':['']}

#Grabs the product details for every product on the page and adds each product as a row in our dataframe
for product in product_card:
    try:
        link = product.find('a', class_ = 'product-card__link-overlay').get('href')
        name = product.find('div', class_ = 'product-card__title').text
        subtitle = product.find('div', class_ = 'product-card__subtitle').text
        full_price = product.find('div', class_ = 'product-price__wrapper css-vxq8l0').text
        sale_price = product.find('div', class_ = 'product-price is--current-price css-1mj7kho').text
        product_dict['Link'].append('https://www.nike.com' + link)
        product_dict['Name'].append(name)
        product_dict['Subtitle'].append(subtitle)
        product_dict['Price'].append(full_price)
        product_dict['Sale Price'].append(sale_price)
    except:
        pass

#print(product_dict)

#exports the dataframe as a csv
products_df = pd.DataFrame(product_dict)
products_df.to_csv('nike_details.csv')
