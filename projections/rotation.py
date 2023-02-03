import time
import openpyxl
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import csv
from datetime import date, timedelta
import datetime
import shutil


def init(link):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'user-agent={user_agent}')

    browser = webdriver.Firefox()
    browser.get(link)
    time.sleep(2)
    return browser


TEAMS = {
    'Diamondbacks': 'ARI',    'Braves': 'ATL',    'Orioles': 'BAL',    'RedSox': 'BOS',    'Cubs': 'CHC',    'WhiteSox': 'CHW',    'Reds': 'CIN',
    'Guardians': 'CLE', 'Rockies': 'COL',    'Tigers': 'DET',    'Astros': 'HOU',    'Royals': 'KCR',    'Angels': 'LAA',    'Dodgers': 'LAD',
    'Marlins': 'MIA',    'Brewers': 'MIL', 'Twins': 'MIN',    'Mets': 'NYM',    'Yankees': 'NYY',    'Athletics': 'OAK',    'Phillies': 'PHI',
    'Pirates': 'PIT',    'Padres': 'SD',    'Mariners': 'SEA', 'Giants': 'SF',    'Cardinals': 'STL',    'Rays': 'TB',    'Rangers': 'TEX',
    'BlueJays': 'TOR',    'Nationals': 'WAS',
}

results = {
    'ARI': [], 'ATL': [], 'BAL': [], 'BOS': [], 'CHC': [], 'CHW': [],
    'CIN': [], 'CLE': [], 'COL': [], 'DET': [], 'HOU': [], 'KCR': [],
    'LAA': [], 'LAD': [], 'MIA': [], 'MIL': [], 'MIN': [], 'NYM': [],
    'NYY': [], 'OAK': [], 'PHI': [], 'PIT': [], 'SD': [], 'SEA': [],
    'SF': [], 'STL': [], 'TB': [], 'TEX': [], 'TOR': [], 'WAS': [],
}

dates = ['03/17/2022', '03/18/2022', '03/19/2022',
         '03/20/2022', '03/21/2022', '03/22/2022', '03/23/2022']


b = init('https://www.baseballpress.com/lineups/2022-04-07')
time.sleep(0.5)
tomorrow = date.today() - timedelta(days=100)
today = date.today()


# dd/mm/YY
end_date = tomorrow.strftime("%m/%d/%Y")
print(end_date)
while True:
    try:
        current_date = b.find_element(
            by=By.CLASS_NAME, value="date-item")
        data = current_date.get_attribute('data-val')
        day_of_week = current_date.text.split(" ")[0]
        print(day_of_week)
        if data == "06/01/2022":
            break
        else:
            lineup_table = b.find_elements(
                by=By.CLASS_NAME, value="lineup-card")
            for i in lineup_table:
                try:
                    cancel = i.find_element(
                        by=By.CLASS_NAME, value="bad-status")
                except:
                    player_list = i.find_elements(
                        by=By.CLASS_NAME, value="player")
                    teams = i.find_elements(
                        by=By.CLASS_NAME, value="mlb-team-logo")
                    team1 = teams[0].get_attribute(
                        'text').replace(" ", "")
                    team1 = team1.replace("\n", "")
                    team2 = teams[1].get_attribute(
                        'text').replace(" ", "")
                    team2 = team2.replace("\n", "")
                    starter1 = player_list[0].text
                    starter2 = player_list[1].text
                    # print(team1+starter1)
                    # print(team2 + starter2)
                    results[TEAMS[team1]].append(starter1)
                    results[TEAMS[team2]].append(starter2)

            next_page = b.find_element(
                by=By.CLASS_NAME, value="fa-arrow-right")
            next_page.click()
            today = today + timedelta(days=1)
            time.sleep(0.2)

    except Exception as e:
        print(e)
        break

for team in results:
    print(team + "===" + str(results[team]))

with open('rotation.csv', 'w', newline='') as csvfile:
    for team in results:
        writer = csv.writer(csvfile)
        writer.writerow([team] + results[team])
