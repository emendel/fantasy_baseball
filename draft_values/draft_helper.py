from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
import time
import pickle
import math
import sys
import itertools
import numpy as np
import pandas as pd


def init(link):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'user-agent={user_agent}')

    browser = webdriver.Firefox()
    browser.get(link)
    time.sleep(2)
    return browser


BATTING_TARGETS = [1100, 320, 1080, 140, 0.8]
PITCHING_TARGETS = [105, 75, 1440, 3.4, 1.17, 20]
# PITCHER_STATS = [0, row.SV, 0, row.ERA, row.IP]
# BATTER_STATS = [row.R, row.HR, row.RBI, row.SB, row.OPS]
PITCH_CATS = ["QS", "SV", "SO", "ERA", "WHIP", "IP", "G"]

MY_TEAM = [0, 0, 0, 0, 0]


def best_players():
    # df = pd.read_excel('top_200_batters.xlsx')
    df = pd.read_excel('top_400_pitchers.xlsx')
    df2 = df.sort_values(by=["QS"], ascending=False).head(80)
    qs_avg = df2["QS"].mean()
    qs_std = df2["QS"].std()
    df2 = df.sort_values(by=["SO"], ascending=False).head(80)
    so_avg = df2["SO"].mean()
    so_std = df2["SO"].std()
    df2 = df.sort_values(by=["SV"], ascending=False).head(40)
    sv_avg = df2["SV"].mean()
    sv_std = df2["SV"].std()
    df2 = df.sort_values(by=["WHIP"], ascending=True).head(105)
    whip_avg = df2["WHIP"].mean()
    whip_std = df2["WHIP"].std()
    df2 = df.sort_values(by=["ERA"], ascending=True).head(105)
    era_avg = df2["ERA"].mean()
    era_std = df2["ERA"].std()
    ip_avg = df.sort_values(by=["IP"], ascending=False).head(80)["IP"].mean()
    ip_std = df.sort_values(by=["IP"], ascending=False).head(80)["IP"].std()
    print("qs", qs_avg, qs_std)
    print("so", so_avg, so_std)
    print("sv", sv_avg, sv_std)
    print("whip", whip_avg, whip_std)
    print("era", era_avg, era_std)
    print("ip", ip_avg, ip_std)

    for i, row in df.iterrows():
        player_stats = [row.QS, row.SV, row.SO,
                        row.ERA, row.WHIP, row.IP, row.G]
        df.loc[(i, 'VALUE')] = calculate_value_pitcher(
            player_stats, PITCHING_TARGETS)
        df.loc[(i, 'QS_VALUE')] = (row.QS - qs_avg) / qs_std
        df.loc[(i, 'SO_VALUE')] = (row.SO - so_avg) / so_std
        df.loc[(i, 'SV_VALUE')] = (row.SV - sv_avg) / sv_std
        # player_stats = [row.R, row.HR, row.RBI, row.SB, row.OPS]
        # df.loc[(i, 'VALUEOPS')] = calculate_value_batter(
        #     player_stats, BATTING_TARGETS)

    cost_map = average_cost()
    for x in cost_map.keys():
        df.loc[df['Name'] == x, 'Dollars'] = cost_map[x]

    df.to_excel('pitchrs_with_values.xlsx')


def calculate_value_pitcher(player, targets):
    qs = player[0] / targets[0] * 100 if player[0] else 0
    saves = player[1] / targets[1] * 100 if player[1] else 0
    so = player[2] / targets[2] * 100 if player[2] else 0
    era = whip = 0
    ip_weight = (player[5]/player[6]) / targets[5]
    era = (targets[3] - player[3]) * ip_weight * 100
    whip = (targets[4] - player[4]) * ip_weight * 100
    # era = ip_weight * player[3]
    # era = player[3] / targets[3] * 100 if player[3] else 0
    # whip = player[4] / targets[4] * 100 if player[4] else 0
    return qs+saves+so+era+whip


def calculate_value_batter(player, targets):
    runs = player[0] / targets[0] * 100 if player[0] else 0
    hr = player[1] / targets[1] * 100 if player[1] else 0
    rbi = player[2] / targets[2] * 100 if player[2] else 0
    steals = player[3] / targets[3] * 100 if player[3] else 0
    ops = player[4] / targets[4] * 100 if player[4] else 0
    return runs+hr+rbi+steals+ops


def average_cost():
    players_with_cost = {}
    browser = init(
        'https://baseball.fantasysports.yahoo.com/b1/23743/draftanalysis?type=salcap')
    action = ActionChains(browser)
    action.send_keys("ezra.mendelson", Keys.ENTER)
    action.perform()
    time.sleep(1)

    action2 = ActionChains(browser)
    action2.send_keys("6JWr7R4RMB5dRyw", Keys.ENTER)
    action2.perform()
    time.sleep(5)
    for x in range(0, 8):
        players = browser.find_elements(by=By.TAG_NAME, value="tr")
        names = browser.find_elements(
            by=By.XPATH, value="//*[@data-tst='player-name']")
        # dollars = browser.find_elements(by=By.CLASS_NAME, value="Ta(c)")
        # print(len(dollars))
        players = players[2:]
        count = 0
        for p in players:
            name = names[count].text
            count += 1
            dollars = p.find_elements(By.TAG_NAME, "td")[
                5].find_element(By.TAG_NAME, 'div').text
            # print(name, dollars)
            players_with_cost[name] = dollars
        browser.find_element(
            by=By.XPATH, value="//*[@data-icon='caret-right']").click()
        time.sleep(1)
    return players_with_cost


# def find_best_team(df, salary_cap):
#     best_team = None
#     best_score = 0
#     for team in itertools.combinations(df.index, 13):
#         print(team)
#         # salary = 0
#         # score = 0
#         # names = []
#         # for x in team:
#         #     salary += df.loc[(x, 'Dollars')]
#         #     score += df.loc[(x, 'VALUE')]
#         #     names.append(df.loc[(x, 'Name')])
#         # if salary <= salary_cap:
#         #     if score > best_score:
#         #         best_score = score
#         #         best_team = team
#         #         print("++++++")
#         #         print(names)
#     return df.loc[best_team, :]


def find_best_team(df, salary_cap):
    max_points = -np.inf
    best_team = []
    df2 = df[['Dollars', 'VALUEOPS', 'Name']].copy()
    print(df2)

    def branch_and_bound(start, remaining, salary, points, depth):
        nonlocal max_points, best_team

        # Check if we have reached the desired depth
        if depth == 15:
            # print("salary", salary)
            # print("points", points)
            # print("max_points", max_points)
            if points > max_points and salary <= salary_cap:
                print(best_team)
                print("+++++++++++++", points, salary)
                max_points = points
                best_team = start
            return

        for i, player in enumerate(remaining):
            if salary + player['Dollars'] > salary_cap:
                continue
            branch_and_bound(start + [player], remaining[i+1:], salary +
                             player['Dollars'], points + player['VALUEOPS'], depth + 1)

    branch_and_bound([], df2.to_dict(orient='records'), 0, 0, 0)
    return best_team


if __name__ == '__main__':
    best_players()
    # df = pd.read_excel('top_200_with_values.xlsx')
    # df.sort_values(by=['VALUEOPS'])
    # max_sum, subarr = max_sum_subarray(df, 13, 260)

    # print(find_best_team(df, 200))
