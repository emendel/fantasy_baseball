import math
import pickle
import time
from auto_application_helpers import init
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
import json
import csv
import sys


def init(link):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'user-agent={user_agent}')

    browser = webdriver.Firefox()
    browser.get(link)
    time.sleep(2)
    return browser


fn = "catalog.csv"
dic = {}
lis = []
products = []
search = []
b = init('https://www.rotochamp.com/default.aspx')
time.sleep(3)
cnt = 0
with open("batters.csv", "r") as inf,  \
        open('batters_dollars.csv', 'w', newline='') as outf:
    csvreader = csv.DictReader(inf)
    # Add column name to beginning.
    fieldnames = csvreader.fieldnames
    csvwriter = csv.DictWriter(outf, fieldnames)
    csvwriter.writeheader()
    for row in csvreader:
        card = {
            "Name": row["Name"],
            "HR": row["HR"],
            "R": row["R"],
            "RBI": row["RBI"]
            # "QS": row["QS"],
            # "SV": row["SV"],
            # "SO": row["SO"]
        }
        query = card["Name"]
        searchbar = b.find_element(by=By.ID, value="inputPlayerSearch")
        searchbar.click()
        action = ActionChains(b)
        action2 = ActionChains(b)
        action.send_keys(query)
        time.sleep(1)
        action.perform()
        time.sleep(1)
        action2.send_keys(Keys.DOWN, Keys.ENTER)
        time.sleep(1)
        action2.perform()
        time.sleep(2)
        dollars = []
        cnt = 0
        composite = ''
        past = ''
        try:
            table = b.find_elements(by=By.CLASS_NAME, value="hidden-xs")
            for x in table:
                if '$' in x.text:
                    if cnt == 0:
                        composite = x.text.replace("$", "")
                        composite = composite.replace("(", "-")
                        composite = composite.replace(")", "")
                    if cnt > 0 and cnt < 6:
                        d = x.text.replace("$", "")
                        d = d.replace("(", "-")
                        d = d.replace(")", "")
                        dollars.append(float(d))
                    if cnt == 6:
                        past = x.text.replace("$", "")
                        past = past.replace("(", "-")
                        past = past.replace(")", "")
                    cnt += 1
            dollars.sort()
            median = dollars[int(len(dollars)/2)]
            card["HR"] = median
            card["R"] = float(composite)
            card["RBI"] = float(past)
            # card["QS"] = median
            # card["SV"] = float(composite)
            # card["SO"] = float(past)

        except Exception as e:
            print(e)
            continue

        print(query + "===" + str(median))
        csvwriter.writerow(card)
