from selenium import webdriver
from tempfile import mkdtemp
import sqlalchemy
import requests
import numpy as np
import pandas as pd
import datetime
import json
import urllib
from sqlalchemy import create_engine
from selenium_stealth import stealth
import pymysql


URL_SEARCH = "https://www.tickpick.com/concerts/yeat-tickets/"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280x1696")
options.add_argument("--single-process")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-dev-tools")
options.add_argument("--no-zygote")
options.add_argument(f"--user-data-dir={mkdtemp()}")
options.add_argument(f"--data-path={mkdtemp()}")
options.add_argument(f"--disk-cache-dir={mkdtemp()}")
options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome(r"C:\Users\Paul\Documents\chromedriver.exe", options=options)

stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
    )

driver.get(URL_SEARCH)

xpath_links = "//*[@id=\"events\"]/div[*]/a[1]"

links = driver.find_elements_by_xpath(xpath_links)

venue_names = driver.find_elements_by_xpath("//*[@id=\"events\"]/div[*]/div[2]/span/span")
dates = driver.find_elements_by_xpath("//*[@id=\"events\"]/div[*]/div[1]/span[1]")

links = list(map(lambda elem: elem.get_attribute("href"), links))
venue_names = list(map(lambda elem: elem.text, venue_names))
dates = list(map(lambda elem: elem.text, dates))

def add_page_to_row_list(link, row_list, driver, venue_name, date, time):
    driver.get(link)

    xpath = "//*[@id=\"listingContainer\"]/div[*]"

    elements = []

    while len(elements) == 0:
        elements = driver.find_elements_by_xpath(xpath)

    for elem in elements:
        dic = {}
        dic["Date"] = time
        dic["VenueID"] = venue_name
        dic["DateEvent"] = date
        dic["Quantity"] = elem.find_element_by_tag_name("select").text.split()[0]
        dic["Price"] = elem.find_element_by_tag_name("b").text[1:]
        row_list.append(dic)

row_list = []

date = datetime.datetime.now()
time = date.strftime("%m.%d.%y_%H.%M")

for i in range(len(links)):
    print(links[i])
    add_page_to_row_list(links[i], row_list, driver, venue_names[i], dates[i], time)

df = pd.DataFrame(row_list)
df.head()

df["Price"].head(100)

server = 'tickpick-scraper-database.mysql.database.azure.com'
database = 'tickpick_database'
username = 'pauldoucet'
driver = '{ODBC Driver 17 for SQL Server}'
ca_path = "DigiCertGlobalRootCA.crt.pem"

f = open("password.json")
data = json.load(f)
password = data["password"]

sqlUrl = URL(
    drivername="mysql+pymysql",
    username=username,
    password=password,
    host=server,
    port=3306,
    database=database,
    query={"ssl_ca": ca_path},
)
engine = create_engine(sqlUrl)

df.to_sql("test_table", con=engine, if_exists="append", index=False)