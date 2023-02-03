import pandas as pd
BATTING_TARGETS = [1100, 320, 1080, 140, 0.8]


MELENDEZ = [60, 20, 61, 4, 0.738]
ABREU = [84, 23, 82, 0, 0.81]
TUCKER = [95,	32,	95,	21,	0.841]
SOTO = [100,	30,	90,	8,	0.932]

players = [MELENDEZ, ABREU, SOTO, TUCKER]

current_totals = [0, 0, 0, 0, 0]


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

    batters_df.to_excel('top_200_with_values.xlsx')


def calculate_value(player, targets):
    runs = player[0] / targets[0] * 100 if player[0] else 0
    hr = player[1] / targets[1] * 100 if player[1] else 0
    rbi = player[2] / targets[2] * 100 if player[2] else 0
    steals = player[3] / targets[3] * 100 if player[3] else 0
    ops = player[4] / targets[4] * 100 if player[4] else 0
    return runs+hr+rbi+steals+ops


best_players()
