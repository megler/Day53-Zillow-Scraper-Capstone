# zillowScraper.py
#
# Python Bootcamp Day 53 - Zillow Data Scraper
# Usage:
#      Given a set of parameters, scrape Zillow and fill out Google Form with
# gathered data.
#
# Marceia Egler December 29, 2021

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import json


load_dotenv()

service = Service(os.environ.get("DRIVER"))
driver = webdriver.Chrome(service=service)
driver.get(os.environ.get("FORM_URL"))

zillow_url = os.environ.get("ZILLOW_URL")
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Accept-Language": "en-US,en;q=0.5",
}

r = requests.get(zillow_url, headers=header)
zillow_results = r.text
soup = BeautifulSoup(zillow_results, "html.parser")

data = json.loads(
    soup.select_one("script[data-zrr-shared-data-key]")
    .contents[0]
    .strip("!<>-")
)

# get house links
house_links = [
    result["detailUrl"]
    for result in data["cat1"]["searchResults"]["listResults"]
]

# amend house_links to have all proper URLS
house_links = [
    link.replace(link, "https://www.zillow.com" + link)
    if not link.startswith("http")
    else link
    for link in house_links
]

# Get address
house_address = [
    result["address"]
    for result in data["cat1"]["searchResults"]["listResults"]
]

# Get price
house_rent = [
    int(result["units"][0]["price"].strip("$").replace(",", "").strip("+"))
    if "units" in result
    else result["unformattedPrice"]
    for result in data["cat1"]["searchResults"]["listResults"]
]


def fill_form():
    """Open Google Form, fill each field with scraped data, submitting after each entry."""
    for i in range(len(house_address)):
        driver.get(os.environ.get("FORM_URL"))
        fill_address = driver.find_element(
            By.XPATH,
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input',
        )
        fill_address.send_keys(house_address[i])

        fill_rent = driver.find_element(
            By.XPATH,
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input',
        )
        fill_rent.send_keys(house_rent[i])

        fill_link = driver.find_element(
            By.XPATH,
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input',
        )
        fill_link.send_keys(house_links[i])

        submit_button = driver.find_element(
            By.XPATH,
            '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span',
        )
        submit_button.click()
    driver.quit()


fill_form()
