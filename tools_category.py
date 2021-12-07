from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

driver_path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'browser':'ALL' }
driver = webdriver.Chrome(executable_path=driver_path, desired_capabilities=d)

driver.get('https://toolshed.g2.bx.psu.edu/repository/browse_categories?message=&status=done')

# Wait for the JS loading data
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "grid-table-body"))
)
# time.sleep(10)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
body = soup.find(id="grid-table-body")
trs = body.find_all('tr')

category_list = []
url_list = []
description_list = []
repository_list = []

for i in trs:
    try:
        tds = i.find_all('td')
        category = ''
        url = ''
        description = ''
        repositories = ''
        for id in range(3):
            if id == 0:
                category = tds[0].text
                url = tds[0].find('a').get('href')
            elif id == 1:
                description =tds[id].text
            else:
                repositories = tds[id].text
        if category != '':
            category_list.append(category)
            url_list.append(url)
            description_list.append(description)
            repository_list.append(repositories)
            print('Category:', category)
            print('URL:', url)
            print()
    except AttributeError as e:
        continue

df = pd.DataFrame(list(zip(category_list, url_list, description_list, repository_list)),
                  columns=['category', 'url', 'description', 'repostories'])
df.to_csv('./tools/category.csv', header=False, index=False)
print("over")

