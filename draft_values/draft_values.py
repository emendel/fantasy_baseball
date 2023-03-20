import math
import time
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import csv

invalid_chars = ['á', 'í', 'é', 'ó', 'ú', 'ñ', 'Á', 'Í', 'É', 'Ó', 'Ú', 'Ñ']
valid_chars = ['a', 'i', 'e', 'o', 'u', 'n', 'A', 'I', 'E', 'O', 'U', 'N']
pitchers = []
batters = []
p_cost = []
b_cost = []


def init(link):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'user-agent={user_agent}')

    browser = webdriver.Firefox()
    browser.get(link)
    time.sleep(1)
    return browser


def main():
    browser = get_browser_session()
    players = browser.find_elements(by=By.CLASS_NAME, value='player')
    cost = browser.find_elements(by=By.CLASS_NAME, value='cost')
    cost_index = 0
    for p in players:
        name = p.text.split('(')[0]
        name = name[:-1]
        for x in range(0, len(invalid_chars)):
            name.replace(invalid_chars[x], valid_chars[x])
        if "- P" in p.text:
            pitchers.append(name)
            p_cost.append(cost[cost_index].text)

        else:
            batters.append(name)
            b_cost.append(cost[cost_index].text)

        cost_index += 1
    write_draft('b', batters)
    write_draft('p', pitchers)


def write_draft(file, players):
    index = 0
    costs = p_cost
    if file == 'b':
        costs = b_cost
    with open('{}_draft_value.csv'.format(file), 'w', newline='') as outf:
        # Add column name to beginning.
        fieldnames = ["Name", "FVAL"]
        csvwriter = csv.DictWriter(outf, fieldnames)
        csvwriter.writeheader()
        for player in players:
            card = {"Name": player,
                    "FVAL": costs[index]}
            index += 1
            csvwriter.writerow(card)


def get_browser_session():
    browser = init(
        'https://baseball.fantasysports.yahoo.com/2022/b1/33734/draftresults?pspid=97444672&activity=draftresults')
    action = ActionChains(browser)
    action.send_keys("ezra.mendelson", Keys.ENTER)
    action.perform()
    time.sleep(2)

    action2 = ActionChains(browser)
    action2.send_keys("6JWr7R4RMB5dRyw", Keys.ENTER)
    action2.perform()
    time.sleep(5)
    return browser


main()
