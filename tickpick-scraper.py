#!/usr/bin/env python
# coding: utf-8

# In[77]:


import requests
from selenium import webdriver
import numpy as np
import pandas as pd
import datetime

URL_SEARCH = "https://www.tickpick.com/concerts/yeat-tickets/"


# In[78]:


driver = webdriver.Chrome(r"C:\Users\Paul\Documents\chromedriver.exe")
driver.get(URL_SEARCH)

xpath_links = "//*[@id=\"events\"]/div[*]/a[1]"


links = driver.find_elements_by_xpath(xpath_links)
venue_names = driver.find_elements_by_xpath("//*[@id=\"events\"]/div[*]/div[2]/span/span")
dates = driver.find_elements_by_xpath("//*[@id=\"events\"]/div[*]/div[1]/span[1]")

links = list(map(lambda elem: elem.get_attribute("href"), links))
venue_names = list(map(lambda elem: elem.text, venue_names))
dates = list(map(lambda elem: elem.text, dates))


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




