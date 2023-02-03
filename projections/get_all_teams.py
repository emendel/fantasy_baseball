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
players = []


def init(link):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'user-agent={user_agent}')

    browser = webdriver.Firefox()
    browser.get(link)
    time.sleep(1)
    return browser


invalid_chars = ['á', 'í', 'é', 'ó', 'ú', 'ñ', 'Á', 'Í', 'É', 'Ó', 'Ú', 'Ñ']
valid_chars = ['a', 'i', 'e', 'o', 'u', 'n', 'A', 'I', 'E', 'O', 'U', 'N']


def main():
    browser = setup_browser_session()
    for value in range(1, 15):
        player_names = []
        browser.get(
            'https://baseball.fantasysports.yahoo.com/b1/33734/{}'.format(value))
        players = browser.find_elements(
            by=By.CLASS_NAME, value='Nowrap')
        print(len(players))

        for x in range(0, len(players)):
            if "- P" in players[x].text:
                l = players[x].text.split(" ")
                name = l[0] + " " + l[1]
                for x in range(0, len(invalid_chars)):
                    name = name.replace(
                        invalid_chars[x], valid_chars[x])
                if 'Empty' not in name:
                    player_names.append(name)
                    print(name)
        write_team(value, player_names)


def write_team(team_name, players):
    with open('all_teams/p_team_{}.csv'.format(team_name), 'w', newline='') as outf:
        # Add column name to beginning.
        fieldnames = ["Name", "HR", "R", "RBI", "SB", "OPS", "AB", "FVAL"]
        csvwriter = csv.DictWriter(outf, fieldnames)
        csvwriter.writeheader()
        for player in players:
            card = {"Name": player}
            csvwriter.writerow(card)


def setup_browser_session():
    browser = init(
        'https://baseball.fantasysports.yahoo.com/b1/33734/1')

    action = ActionChains(browser)
    action.send_keys("ezra.mendelson", Keys.ENTER)
    action.perform()
    time.sleep(1)

    action2 = ActionChains(browser)
    action2.send_keys("6JWr7R4RMB5dRyw", Keys.ENTER)
    action2.perform()
    time.sleep(5)
    return browser


main()
