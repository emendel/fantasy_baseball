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


pitchers = True


def main():
    if pitchers:
        print('Name,QS,SV,SO,ERA,WHIP,IP,FVAL')
    else:
        print('Name,HR,R,RBI,SB,OPS,AB,FVAL')
    toggle = False

    browser = get_free_agents_browser_session()

    if pitchers:
        button = browser.find_element(
            by=By.XPATH, value="//*[contains(text(), 'All Batters')]")
        button.click()
        time.sleep(0.2)
        button2 = browser.find_element(
            by=By.XPATH, value="//*[contains(text(), 'All Pitcher')]")
        button2.click()
        time.sleep(0.2)
        action2 = ActionChains(browser)
        action2.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER)
        action2.perform()
        time.sleep(5)

    clicks = 4
    rostered_button = browser.find_element(
        by=By.XPATH, value="//*[contains(text(), 'IP*')]")
    rostered_button.click()
    time.sleep(1)
    while clicks != 0:
        table = browser.find_elements(by=By.ID, value='players-table')
        a_list = []
        for a in table:
            a_list.extend(a.find_elements(by=By.TAG_NAME, value='a'))

        i = 0
        for a in a_list:
            if i > 14:
                if len(a.text) >= 9 or 'Video' in a.text:
                    player_name = a.text
                    # try:
                    for x in range(0, len(invalid_chars)):
                        player_name = player_name.replace(
                            invalid_chars[x], valid_chars[x])
                    if player_name != "Previous 25":
                        players.append(player_name)
                        print(player_name+'')
                    # except:
                    #     print('failed')
            i += 1
        next25 = browser.find_element(
            by=By.XPATH, value="//*[contains(text(), 'Next 25')]")
        next25.click()
        clicks -= 1
        time.sleep(5)


def get_free_agents_browser_session():
    browser = init(
        'https://baseball.fantasysports.yahoo.com/b1/33734/players?pspid=782201796&activity=players')
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
