from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_tools_by_category(url, category):
    print(url)
    driver.get(url)
    # Wait for the JS loading data
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "grid-table-body"))
    )
    name_list = []
    synopsis_list = []
    owner_list = []
    # time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    footer = soup.find(id="page-link-container")
    if footer is not None:
        pages = len(list(footer.children)) - 1
    else:
        pages = 1
    print(category+"has" + str(pages) +" pages")
    page = 1
    while page <= pages:
        print(page)
        print()
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "grid-table-body"))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find(id="grid-table-body")
        trs = body.find_all('tr')
        for i in trs:
            try:
                tds = i.find_all('td')
                name = tds[0].text
                synopsis = tds[1].text
                owner = tds[4].text
                if name != '':
                    name_list.append(name)
                    synopsis_list.append(synopsis)
                    owner_list.append(owner)
            except AttributeError:
                continue
        page += 1
        if page <= pages:
            # driver.find_element_by_xpath("//a[@page_num=" + str(page) + "]").click()
            driver.get(url+"&message=&status=done&page="+str(page))

    df = pd.DataFrame(list(zip(name_list, synopsis_list, owner_list)),
                      columns=['name', 'synopsis', 'owner'])
    df.to_csv('./' + category + '.csv', header=False, index=False, encoding='utf-8')
    print("over")


# enable browser logging
driver_path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = {'browser': 'ALL'}
# driver = webdriver.Chrome(desired_capabilities=d)
driver = webdriver.Chrome(executable_path=driver_path, desired_capabilities=d)

base_url = 'https://toolshed.g2.bx.psu.edu'

df = pd.read_csv('./tools/category.csv', header=None)
category_list = df[0]
url_list = df[1]

for i in range(len(url_list)):
    get_tools_by_category(base_url + url_list[i], category_list[i])
# load the desired webpage
