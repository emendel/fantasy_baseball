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
MY_TEAM = [0, 0, 0, 0, 0]


def best_players():
    batters_df = pd.read_excel('top_200_batters.xlsx')
    # batters_df[]
    for i, row in batters_df.iterrows():
        player_stats = [row.R, row.HR, row.RBI, row.SB, 0]
        batters_df.loc[(i, 'VALUE')] = calculate_value(
            player_stats, BATTING_TARGETS)
        player_stats = [row.R, row.HR, row.RBI, row.SB, row.OPS]
        batters_df.loc[(i, 'VALUEOPS')] = calculate_value(
            player_stats, BATTING_TARGETS)

    cost_map = average_cost()
    for x in cost_map.keys():
        batters_df.loc[batters_df['Name'] == x, 'Dollars'] = cost_map[x]

    batters_df.to_excel('top_200_with_values.xlsx')


def calculate_value(player, targets):
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


def max_sum_subarray(df, k, cost_limit):
    VALUE = 'VALUEOPS'
    DOLLARS = 'Dollars'
    max_sum = 0
    current_sum = 0
    subarray = []
    max_array = []
    current_cost = 0
    max_sum = 0
    i = 0
    # for i, row in df.iterrows():
    while i < len(df):
        # print(subarray)
        row = df.loc[i]
        if current_sum == 0:
            current_sum += row[VALUE]
            current_cost += row[DOLLARS]
            subarray.append(
                {"name": row["Name"], "cost": row["Dollars"], "value": row[VALUE], "index": row["#"]})
        elif current_cost + row[DOLLARS] <= cost_limit:
            current_sum += row[VALUE]
            current_cost += row[DOLLARS]
            subarray.append(
                {"name": row["Name"], "cost": row["Dollars"], "value": row[VALUE], "index": row["#"]})
        if len(subarray) == 13:
            if current_sum > max_sum:
                max_sum = current_sum
                max_array = subarray
                print("new best ++++++++++", current_sum, current_cost)
                for x in subarray:
                    print(x)
            elem = subarray.pop()
            index = elem['index']
            i = index - 1
            current_cost -= elem['cost']
            current_sum -= elem['value']

            # return 0, subarray
        elif i == len(df) - 1 and len(subarray) != 13:
            elem = subarray.pop()
            index = elem['index']
            i = index - 1
            current_cost -= elem['cost']
            current_sum -= elem['value']
        i += 1

    print(len(df))

    return max_array, subarray


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


# def find_best_team(df, salary_cap):
#     num_players = df.shape[0]

#     # Define the objective function
#     c = df['VALUE'].to_numpy()
#     A_ub = np.array([df['Dollars'].to_numpy()])
#     b_ub = np.array([salary_cap])

#     # Define the bounds for each decision variable
#     bounds = [(0, 1) for i in range(num_players)]

#     # Solve the linear programming problem
#     res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='simplex',
#                   options={"disp": False})

#     # Extract the team with the highest points
#     team = df[res.x >= 1.0 / num_players].copy()
#     return team


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
    df = pd.read_excel('top_200_with_values.xlsx')
    # df.sort_values(by=['VALUEOPS'])
    # max_sum, subarr = max_sum_subarray(df, 13, 260)

    print(find_best_team(df, 200))
    # for x in subarr:
    #     print(x)
    # print("+++++++++++++")
    # for x in max_sum:
    #     print(x)
