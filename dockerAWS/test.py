from selenium import webdriver
from tempfile import mkdtemp
import sqlalchemy
import numpy as np
import pandas as pd
import datetime
import json
import urllib
from sqlalchemy import create_engine
import pymysql
import undetected_chromedriver as uc
from sqlalchemy.engine.url import URL
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import requests

def handler(event=None, context=None):

    display = Display(visible=0, size=(1920, 1920))
    display.start()

    URL_SEARCH = "https://www.tickpick.com/concerts/yeat-tickets/"

    options = uc.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")

    driver = uc.Chrome(options=options)

    print("driver started")

    driver.get(URL_SEARCH)

    print("fetched url, fetching links")

    print(driver.page_source)

    xpath_links = "//*[@id=\"events\"]/div[*]/a[1]"

    links = []
    while(not(links)):
        links = driver.find_elements_by_xpath(xpath_links)

    venue_names = driver.find_elements_by_xpath("//*[@id=\"events\"]/div[*]/div[2]/span/span")
    dates = driver.find_elements_by_xpath("//*[@id=\"events\"]/div[*]/div[1]/span[1]")

    links = list(map(lambda elem: elem.get_attribute("href"), links))
    venue_names = list(map(lambda elem: elem.text, venue_names))
    dates = list(map(lambda elem: elem.text, dates))

    print(links)

    API_URL = 'https://api.tickpick.com/1.0/listings/internal/event/'

    date = datetime.datetime.now()
    time = date.strftime("%b %d %I:%M%p")

    def scrap_page(url, date, venue_name, time):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        id = re.findall('https://www.tickpick.com/[^/]+/([^/]+)/', url)[0]
        r = requests.get(API_URL + id)
        soup = BeautifulSoup(r.content, 'html.parser')
        content = json.loads(soup.prettify())
        for ticket in content:
            dic = {}
            dic['Date'] = time
            dic['VenueID'] = venue_name
            dic['DateEvent'] = date
            dic['Quantity'] = ticket['sp'][0]
            dic['Price'] = int(ticket['p'])
            row_list.append(dic)

    row_list = []

    for i in range(len(dates)):
        print(links[i])
        scrap_page(links[i], dates[i], venue_names[i], time)

    df = pd.DataFrame(row_list)
    df.head()

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