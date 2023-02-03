import time
import csv
from datetime import date, timedelta
import datetime
import shutil
import pandas as pd
import numpy as np
from statistics import mean
from pybaseball import pitching_stats, playerid_lookup, statcast_pitcher, pitching_stats_bref, team_batting, team_pitching, batting_stats


TEAMS_MAPPING = {
    'Arizona': 'ARI',
    'Atlanta': 'ATL',
    'Baltimore': 'BAL',
    'Boston': 'BOS',
    'Chi. Cubs': 'CHC',
    'Chi. White Sox': 'CHW',
    'Cincinnati': 'CIN',
    'Cleveland': 'CLE',
    'Colorado': 'COL',
    'Detroit': 'DET',
    'Houston': 'HOU',
    'Kansas City': 'KC',
    'L.A. Angels': 'LAA',
    'L.A. Dodgers': 'LAD',
    'Miami': 'MIA',
    'Milwaukee': 'MIL',
    'Minnesota': 'MIN',
    'N.Y. Mets': 'NYM',
    'N.Y. Yankees': 'NYY',
    'Oakland': 'OAK',
    'Philadelphia': 'PHI',
    'Pittsburgh': 'PIT',
    'San Diego': 'SD',
    'Seattle': 'SEA',
    'San Francisco': 'SF',
    'St. Louis': 'STL',
    'Tampa Bay': 'TB',
    'Texas': 'TEX',
    'Toronto': 'TOR',
    'Washington': 'WAS'
}

TEAMS = {
    'ARI': 4.33,
    'ATL': 4.83,
    'BAL': 4.16,
    'BOS': 4.54,
    'CHC': 4.06,
    'CHW': 4.23,
    'CIN': 4.00,
    'CLE': 4.23,
    'COL': 4.31,
    'DET': 3.44,
    'HOU': 4.51,
    'KC': 3.95,
    'LAA': 3.85,
    'LAD': 5.17,
    'MIA': 3.62,
    'MIL': 4.48,
    'MIN': 4.30,
    'NYM': 4.73,
    'NYY': 4.68,
    'OAK': 3.51,
    'PHI': 4.59,
    'PIT': 3.65,
    'SD': 4.34,
    'SEA': 4.27,
    'SF': 4.42,
    'STL': 4.73,
    'TB': 4.07,
    'TEX': 4.36,
    'TOR': 4.78,
    'WAS': 3.72
}

AWAY_TEAMS = {
    'ARI': 4.31,
    'ATL': 4.80,
    'BAL': 4.10,
    'BOS': 4.23,
    'CHC': 4.11,
    'CHW': 4.38,
    'CIN': 3.45,
    'CLE': 4.51,
    'COL': 2.99,
    'DET': 3.40,
    'HOU': 4.47,
    'KC': 3.77,
    'LAA': 3.62,
    'LAD': 5.17,
    'MIA': 3.58,
    'MIL': 4.48,
    'MIN': 4.36,
    'NYM': 4.89,
    'NYY': 4.72,
    'OAK': 3.87,
    'PHI': 4.24,
    'PIT': 3.43,
    'SD': 4.93,
    'SEA': 4.65,
    'SF': 4.36,
    'STL': 4.69,
    'TB': 3.99,
    'TEX': 4.51,
    'TOR': 5.14,
    'WAS': 3.78
}

HOME_TEAMS = {
    'ARI': 4.36,
    'ATL': 4.87,
    'BAL': 4.23,
    'BOS': 4.84,
    'CHC': 4.00,
    'CHW': 4.09,
    'CIN': 4.56,
    'CLE': 3.95,
    'COL': 5.63,
    'DET': 3.48,
    'HOU': 4.56,
    'KC': 4.14,
    'LAA': 4.07,
    'LAD': 5.18,
    'MIA': 3.65,
    'MIL': 4.47,
    'MIN': 4.23,
    'NYM': 4.57,
    'NYY': 5.06,
    'OAK': 3.14,
    'PHI': 4.94,
    'PIT': 3.86,
    'SD': 3.72,
    'SEA': 3.88,
    'SF': 4.48,
    'STL': 4.76,
    'TB': 4.15,
    'TEX': 4.22,
    'TOR': 4.43,
    'WAS': 3.67
}

players = {}
players_plus = {}
relievers = {}

START_DATE = 'Apr 3'
END_DATE = 'Apr 30'


def calculate_era(location, opponent):
    team = TEAMS_MAPPING[opponent]
    if location == 'vs':
        return AWAY_TEAMS[team]
    else:
        return HOME_TEAMS[team]


with open("sc.csv", newline='') as file:
    result_list = list(csv.reader(file))
    result_2D = np.array(result_list)


for row in range(0, len(result_2D)-1, 2):
    past_todays_date = False
    team = result_2D[row][0]
    for j in range(1, len(result_2D[row])):

        pitcher = result_2D[row][j]
        opponent = result_2D[row+1][j]
        if opponent != '':
            d = opponent.split("/")[1]
            past_todays_date = True if (
                d == START_DATE or past_todays_date == True) else False
            if past_todays_date:
                opponent_location = opponent.split("/")[0]
                opponent = opponent_location[3:]
                location = opponent_location[:2]
                era = '0.0'
                era = calculate_era(location, opponent)
                if pitcher not in players:
                    players[pitcher] = [era]
                else:
                    players[pitcher].append(era)
                if team not in relievers:
                    relievers[team] = [era]
                else:
                    relievers[team].append(era)
                if d == END_DATE:
                    break
        # print("{} {} {} {}".format(pitcher, location, opponent, era))
        pass


# print(result_2D)

bref = pitching_stats_bref(2022)
print(bref[['Name', 'ERA']])
for key in relievers:
    print("{} opponent era: {}".format(key, mean(relievers[key])))


# for key in players:
#     era_to_add = []
#     players_plus[key] = players[key]
#     try:
#         player = bref.loc[bref['Name'] == key]
#         era_to_add = [player.ERA.values[0]]
#         length = len(players[key])
#         temp = players[key].copy()
#         temp.extend(era_to_add*length)
#         players_plus[key] = temp
#         # players[key].extend(era_to_add*length)
#     except Exception as e:
#         print('Lookup failed for ', key)

#     print("{} opponent era: {}".format(key, mean(players[key])))
#     print("{} oppo era+   : {}".format(key, mean(players_plus[key])))

# x = team_batting(2022).columns
# for y in x:
#     print(y)
