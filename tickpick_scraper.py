import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np
import pandas as pd
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

URL_SEARCH = "https://www.tickpick.com/concerts/yeat-tickets/"

options = webdriver.ChromeOptions()
options.binary_location = '/usr/bin/google-chrome'
options.add_argument('headless')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(chrome_options=options)
driver.get(URL_SEARCH)

xpath_links = "//*[@id=\"events\"]/div[*]/a[1]"

links = []
while len(links) == 0:
    links = driver.find_elements(by=By.XPATH, value=xpath_links)
    print(links)

venue_names = driver.find_elements(by=By.XPATH, value="//*[@id=\"events\"]/div[*]/div[2]/span/span")
dates = driver.find_elements(by=By.XPATH, value="//*[@id=\"events\"]/div[*]/div[1]/span[1]")

links = list(map(lambda elem: elem.get_attribute("href"), links))
venue_names = list(map(lambda elem: elem.text, venue_names))
dates = list(map(lambda elem: elem.text, dates))

print(links)



# In[80]:


def add_page_to_row_list(link, row_list, driver, venue_name, date):
    driver.get(link)

    xpath = "//*[@id=\"listingContainer\"]/div[*]"

    elements = []
    
    while len(elements) == 0:
        elements = driver.find_elements_by_xpath(xpath)

    for elem in elements:
        dic = {}
        dic["VenueID"] = venue_name
        dic["Date"] = date
        dic["Quantity"] = elem.find_element_by_tag_name("select").text.split()[0]
        dic["Price"] = elem.find_element_by_tag_name("b").text[1:]
        row_list.append(dic)


# In[79]:


row_list = []

for i in range(len(links)):
    add_page_to_row_list(links[i], row_list, driver, venue_names[i], dates[i])

df = pd.DataFrame(row_list)
date = datetime.datetime.now()
df.to_csv(date.strftime("%m.%d.%y_%H.%M.csv"), index = False)


# In[ ]:




