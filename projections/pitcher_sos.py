import csv
import time
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime

months = {
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10
}

weeks = ["May 15", "May 22", "May 29", "Jun 5", "Jun 12",
         "Jun 19", "Jun 26", "Jul 3", "Jul 10", "Jul 17", "Jul 31"]
end_month = 5
end_day = 22
start_month = 5
start_date = 9


team_runs = {}

teams = {
    "Chicago Cubs": "Chi. Cubs",
    "Chicago White Sox": "Chi. White Sox",
    "New York Mets": "N.Y. Mets",
    "New York Yankees": "N.Y. Yankees",
    "Los Angeles Dodgers": "L.A. Dodgers",
    "Los Angeles Angels": "L.A. Angels",
}

team_runs = {'Arizona': '3.50', 'Atlanta': '3.96', 'Baltimore': '3.38', 'Boston': '3.46', 'Chi. Cubs': '4.17', 'Chi. White Sox': '3.29', 'Cincinnati': '3.16', 'Cleveland': '4.68', 'Colorado': '4.80', 'Detroit': '3.08', 'Houston': '3.81', 'Kansas City': '3.04', 'L.A. Angels': '4.74', 'L.A. Dodgers': '4.96', 'Miami': '3.96',
             'Milwaukee': '4.92', 'Minnesota': '4.23', 'N.Y. Mets': '4.57', 'N.Y. Yankees': '4.76', 'Oakland': '3.68', 'Philadelphia': '4.54', 'Pittsburgh': '3.71', 'San Diego': '4.65', 'Seattle': '4.12', 'San Francisco': '4.48', 'St. Louis': '4.32', 'Tampa Bay': '4.35', 'Texas': '4.33', 'Toronto': '3.78', 'Washington': '4.22'}


def init(link):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'user-agent={user_agent}')

    browser = webdriver.Firefox()
    browser.get(link)
    time.sleep(2)
    return browser


def calculate_sos(opponents):
    l = []
    for x in opponents:
        x = x.replace("@ ", "")
        x = x.replace("vs ", "")
        l.append(float(team_runs[x]))
    return l


def calculate_runs():
    b = init("https://www.baseball-reference.com/leagues/majors/2022.shtml")

    runs_per_game = b.find_elements(
        by=By.XPATH, value="//*[@data-stat='runs_per_game']")
    team_names = b.find_elements(
        by=By.XPATH, value="//*[@data-stat='team_name']")

    for x in range(1, len(runs_per_game)-3):
        if team_names[x].text in teams:
            team_runs[teams[team_names[x].text]] = runs_per_game[x].text
        else:
            l = team_names[x].text.split(" ")
            l.pop()
            text = ' '.join(l)
            team_runs[text] = runs_per_game[x].text


# calculate_runs()
def add_opponent(opponents, opp):
    opponents.append(opp.split('/')[0])

    # if len(opponents) == 0:
    #     opponents.append(opp.split('/')[0])
    # elif opponents[-1] != opp.split('/')[0]:
    #     opponents.append(opp.split('/')[0])


def within_range(schedule_month, schedule_date):
    if schedule_month < start_month:
        return False
    if schedule_month == start_month and schedule_date < start_date:
        return False
    if schedule_month > end_month:
        return False
    if schedule_month == end_month and schedule_date > end_day:
        return False
    return True


with open('schdules.csv') as inf:
    reader = csv.reader(inf, delimiter=',', quotechar='|')
    x = 0
    for row in reader:
        opponents = []
        if (x % 2 == 1):
            team = row.pop(0)
            for opp in row:
                date = opp.split('/')[1]

                schedule_month = months[date.split(" ")[0]]
                schedule_date = int(date.split(" ")[1])
                current_date = datetime.now().day
                current_month = datetime.now().month
                if within_range(schedule_month, schedule_date):
                    add_opponent(opponents, opp)
            runs = calculate_sos(opponents)
            print(team, sum(runs) / len(runs))
        x += 1
