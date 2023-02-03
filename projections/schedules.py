import time
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import csv
from datetime import date, timedelta
import shutil

TEAMS = {
    'arizona-diamondbacks': 'ARI',    'atlanta-braves': 'ATL',    'baltimore-orioles': 'BAL',    'boston-red-sox': 'BOS',    'chicago-cubs': 'CHC',    'chicago-white-sox': 'CHW',
    'cincinnati-reds': 'CIN',    'cleveland-guardians': 'CLE', 'colorado-rockies': 'COL',    'detroit-tigers': 'DET',    'houston-astros': 'HOU',    'kansas-city-royals': 'KC',
    'los-angeles-angels': 'LAA',    'los-angeles-dodgers': 'LAD',    'miami-marlins': 'MIA',    'milwaukee-brewers': 'MIL', 'minnesota-twins': 'MIN',    'new-york-mets': 'NYM',
    'new-york-yankees': 'NYY',    'oakland-athletics': 'OAK',    'philadelphia-phillies': 'PHI',    'pittsburgh-pirates': 'PIT',    'san-diego-padres': 'SD',
    'seattle-mariners': 'SEA', 'san-francisco-giants': 'SF',    'st-louis-cardinals': 'STL',    'tampa-bay-rays': 'TB',    'texas-rangers': 'TEX',
    'toronto-blue-jays': 'TOR',    'washington-nationals': 'WAS',
}

results = {
    'ARI': [], 'ATL': [], 'BAL': [], 'BOS': [], 'CHC': [], 'CHW': [],
    'CIN': [], 'CLE': [], 'COL': [], 'DET': [], 'HOU': [], 'KC': [],
    'LAA': [], 'LAD': [], 'MIA': [], 'MIL': [], 'MIN': [], 'NYM': [],
    'NYY': [], 'OAK': [], 'PHI': [], 'PIT': [], 'SD': [], 'SEA': [],
    'SF': [], 'STL': [], 'TB': [], 'TEX': [], 'TOR': [], 'WAS': [],
}


def init(link):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'user-agent={user_agent}')

    browser = webdriver.Firefox()
    browser.get(link)
    time.sleep(2)
    return browser


browser = init(
    'https://www.google.com')
with open('schdules.csv', 'w') as csvfile:
    for team in TEAMS:
        pitcher_list = []
        browser.get(
            'https://www.cbssports.com/mlb/teams/{}/{}/schedule/'.format(TEAMS[team], team))
        time.sleep(0.2)
        games = browser.find_elements(
            by=By.CLASS_NAME, value='CellLogoNameLockup')
        dates = browser.find_elements(by=By.CLASS_NAME, value='CellGameDate')
        pitching = browser.find_elements(
            by=By.CLASS_NAME, value='CellPlayerName--long')
        print(len(pitching))
        # print(pitching[0].text.split('\n')[0])
        index = 0
        for g in games:
            text = g.text.replace('\n', " ")
            if '@' in text and index*2+2 <= len(pitching):
                pitcher_list.append(
                    pitching[index*2].text.replace("\n", " "))
            elif 'vs' in text and index*2+2 <= len(pitching):
                pitcher_list.append(pitching[index*2].text.replace("\n", " "))

            results[TEAMS[team]].append(
                text + "/" + dates[index].text.split(',')[0])
            index += 1
            # print(text)
        # print(pitcher_list)
        writer = csv.writer(csvfile)
        writer.writerow([TEAMS[team]] + pitcher_list)
        writer.writerow([TEAMS[team]] + results[TEAMS[team]])
