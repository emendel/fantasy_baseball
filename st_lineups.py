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
    'ARI': {}, 'ATL': {}, 'BAL': {}, 'BOS': {}, 'CHC': {}, 'CHW': {},
    'CIN': {}, 'CLE': {}, 'COL': {}, 'DET': {}, 'HOU': {}, 'KCR': {},
    'LAA': {}, 'LAD': {}, 'MIA': {}, 'MIL': {}, 'MIN': {}, 'NYM': {},
    'NYY': {}, 'OAK': {}, 'PHI': {}, 'PIT': {}, 'SD': {}, 'SEA': {},
    'SF': {}, 'STL': {}, 'TB': {}, 'TEX': {}, 'TOR': {}, 'WAS': {},
}

dates = ['03/17/2022', '03/18/2022', '03/19/2022',
         '03/20/2022', '03/21/2022', '03/22/2022', '03/23/2022']


b = init('https://www.baseballpress.com/lineups/2023-02-24')
time.sleep(0.5)
tomorrow = date.today()
today = date.today().strftime('%m-%d-%Y')
print(today)


# dd/mm/YY
d1 = tomorrow.strftime("%m/%d/%Y")
while True:
    try:
        current_date = b.find_element(
            by=By.CLASS_NAME, value="date-item")
        data = current_date.get_attribute('data-val')
        print(data)
        if data == d1:
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
                    for team in range(0, len(teams)):
                        team_name = teams[team].get_attribute('text')
                        # print(team_name)
                        for player in range((9*team)+2, 11+9*team):
                            player_name = player_list[player].text
                            team_name = team_name.replace('\n', '')
                            team_name = team_name.replace(' ', '')
                            p_list = player_name.split(' ')
                            lineup_spot = p_list[0].replace('.', '')
                            position = p_list[len(p_list)-1]
                            name = p_list[1:len(p_list)-2]
                            readable_player_name = ' '.join(name)
                            # print(team_name)
                            # with open(f'lineups/{TEAMS[team_name]}.csv', 'a', newline='') as csvfile:
                            #     fieldnames = dates
                            #     writer = csv.DictWriter(
                            #         csvfile, fieldnames=fieldnames)
                            #     # writer.writeheader()
                            #     string = lineup_spot + ' ' + readable_player_name + ' ' + position
                            #     writer.writerow({data: string})

                            # # print(readable_player_name)
                            # print(lineup_spot, readable_player_name,
                            #       position, team_name)
                            if readable_player_name not in results[TEAMS[team_name]]:
                                results[TEAMS[team_name]][readable_player_name] = {
                                    lineup_spot: 1,
                                    position: 1
                                }
                            else:
                                if lineup_spot not in results[TEAMS[team_name]][readable_player_name]:
                                    results[TEAMS[team_name]
                                            ][readable_player_name][lineup_spot] = 1
                                else:
                                    results[TEAMS[team_name]
                                            ][readable_player_name][lineup_spot] += 1
                                if position not in results[TEAMS[team_name]][readable_player_name]:
                                    results[TEAMS[team_name]
                                            ][readable_player_name][position] = 1
                                else:
                                    results[TEAMS[team_name]
                                            ][readable_player_name][position] += 1
                            # print(player_name, team_name.replace(' ', ''))

            next_page = b.find_element(
                by=By.CLASS_NAME, value="fa-arrow-right")
            next_page.click()
            time.sleep(0.2)

    except Exception as e:
        print(e)
        break

for team in results.keys():
    with open(f'teams/{team}.csv', 'w', newline='') as csvfile:
        fieldnames = ['Player', 'Spot', 'Frequency']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for player in results[team].keys():
            for spot in results[team][player].keys():
                writer.writerow({
                    'Player': player,
                    'Spot': spot,
                    'Frequency': results[team][player][spot]
                })

shutil.make_archive("data/teams-"+today, 'zip', "teams")
