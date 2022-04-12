import requests
import re
from bs4 import BeautifulSoup
import json
import datetime
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import pymysql
import cloudscraper

def handler(event=None, context=None):
	URL_MAIN = 'https://www.tickpick.com/concerts/yeat-tickets/'


	scraper = cloudscraper.create_scraper()

	#r = requests.get(URL_MAIN)
	r = scraper.get(URL_MAIN)

	#soup = BeautifulSoup(r.content, 'html.parser')
	soup = BeautifulSoup(r.text, 'html.parser')

	#return soup.prettify()
	return soup.prettify()

	urls = []
	venue_names = []
	dates = []

	for script in soup.find_all("script", type='application/ld+json'):
	    #print(script.string)
	    if '"@type": "Event"' in script.string:
	        url = re.findall('"url": "([^\s"]*)"', script.string)[0]
	        urls.append(url)

	        venue_name = re.findall('"@type": "EventVenue",[\s]*"name": "([^"]*)"*', script.string)[0]
	        venue_names.append(venue_name)
	        
	        date = re.findall('"startDate": "([^T]*)T', script.string)[0]
	        dates.append(date)

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
	    print(urls[i])
	    scrap_page(urls[i], dates[i], venue_names[i], time)

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

	return row_list

handler()