from bs4 import BeautifulSoup
import requests

#response = requests.get(url=URL,headers=HEADER).text
#soup = BeautifulSoup(response, 'html.parser')
#price = soup.select(" bgp")
#print(response[:2000])

import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

MY_EMAIL = os.getenv("EMAIL_ADDRESS")
PASS = os.getenv("EMAIL_PASSWORD")
HOST = os.getenv("SMTP_ADDRESS")
TO_EMAIL = os.getenv("TO_EMAIL")
URL = "https://es.camelcamelcamel.com/product/B0D1979PLB?context=search"
HEADER = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
}
BUY_PRICE = 16

def get_price():
    driver = webdriver.Chrome()
    driver.get(URL)

    time.sleep(5)
    price_sel = float(driver.find_element(By.CSS_SELECTOR, "span.bgp").text.split("€")[0])
    print(price_sel)

    if price_sel < BUY_PRICE:
        send_low_price_advise()

    driver.quit()

def send_low_price_advise():
    with smtplib.SMTP(HOST, 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASS)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_EMAIL,
            msg=f"Subject:¡Hora de comprar!\n\n "
                f"El funko POP que tanto deseabas está por debajo del precio medio, ¡cómpralo!"
        )

while True:
    ahora = datetime.now()
    if ahora.hour == 9 and ahora.minute == 0:
        get_price()
        time.sleep(3600)

    time.sleep(1)