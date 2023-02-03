import math
import time
from auto_application_helpers import init
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import json


def main():
    players = []
    with open('projections/fa_pitchers.txt') as f:
        content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        players = [x.strip() for x in content]

    toggle = False

    b = init(
        'https://baseballsavant.mlb.com/')

    print('NAME,AVG_EXIT,HARD_HIT,XWOBA,XBA,XSLG,BARREL,K%,BB%')
    for i in range(0, len(players)):
        try:
            result = players[i]
            time.sleep(1)
            searchbar = b.find_element(by=By.ID, value='player-auto-complete')
            searchbar.clear()
            searchbar.send_keys(players[i])
            time.sleep(1)
            action2 = ActionChains(b)
            action2.send_keys(Keys.ENTER)
            action2.perform()
            time.sleep(10)

            #ready = False
            # while not ready:
            #    try:
            #        myElem = WebDriverWait(b, 3).until(EC.presence_of_element_located(
            #            (By.ID, 'text_percent_rank_exit_velocity_avg')))
            #        ready = True
            #        print("Page is ready!")
            #    except TimeoutException:
            #        print("Loading took too much time!")
            #        ready = False
        except:
            print('could not find player')
        try:
            avg_exit = b.find_element(
                by=By.ID, value='text_percent_rank_exit_velocity_avg').text
            result += ',' + avg_exit
        except:
            result += ',XX'
        try:
            hard_hit = b.find_element(
                by=By.ID, value='text_percent_rank_hard_hit_percent').text
            result += ',' + hard_hit
        except:
            result += ',XX'
        try:
            xwoba = b.find_element(
                by=By.ID, value='text_percent_rank_xwoba').text
            result += ',' + xwoba
        except:
            result += ',XX'
        try:
            xba = b.find_element(by=By.ID, value='text_percent_rank_xba').text
            result += ',' + xba
        except:
            result += ',XX'
        try:
            xslg = b.find_element(
                by=By.ID, value='text_percent_rank_xslg').text
            result += ',' + xslg
        except:
            result += ',XX'
        try:
            barrel = b.find_element(
                by=By.ID, value='text_percent_rank_barrel_batted_rate').text
            result += ',' + barrel
        except:
            result += ',XX'
        try:
            krate = b.find_element(
                by=By.ID, value='text_percent_rank_k_percent').text
            result += ',' + krate
        except:
            result += ',XX'
        try:
            bb = b.find_element(
                by=By.ID, value='text_percent_rank_bb_percent').text
            result += ',' + bb
        except:
            result += ',XX'

        # b.get('https://baseballsavant.mlb.com/')
        print(result)


main()
