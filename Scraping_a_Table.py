import requests
from bs4 import BeautifulSoup
import pandas as pd

#Imports the HTML into python
url = 'https://www.worldometers.info/world-population/'
requests.get(url)
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

soup.prettify()

#print(soup)

#Subsets the HTML to only get the HTML of our table needed
table_class = 'datatable w-full border border-zinc-200'
table = soup.find('table', class_ = table_class)

#print(table)

#Gets all the column headers of our table
headers = []
for i in table.find_all('th'):
    title = i.text.strip()
    headers.append(title)
    
#Creates a dataframe using the column headers from our table
df = pd.DataFrame(columns = headers)

#print(df)


#gets all our data within the table and adds it to our dataframe
for j in table.find_all('tr')[1:]:
    row_data = j.find_all('td')
    row = [tr.text for tr in row_data]
    length = len(df)
    df.loc[length] = row
    
#exports the data as a csv
#filepath = 'D:\Projects\Udemy-Web-Scraping-in-python/'
df.to_csv('worlds_population.csv')
