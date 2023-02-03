import pandas as pd
import os



TEAMS = {
    'NYY': ['Gerrit Cole', 'Carlos Rodon', 'Nestor Cortes', 'Luis Severino', 'Frankie Montas'],
    'DET': ['Tarik Skubal', 'Eduardo Rodriguez', 'Spencer Turnbull', 'Matt Manning', 'Alex Faedo']
}

df = pd.read_excel(os.getcwd() + '/schedules.xlsx', header=None)
for team in TEAMS.keys():
    overwritten = False
    l = TEAMS[team] * 36
    del l[-1]
    series = df[0].str.find(team) 
    for x in range(0, len(series)):
        print(series[x])
        if series[x] != -1 and not overwritten:
            df.loc[x] = [team] + l
            overwritten = True


with pd.ExcelWriter(os.getcwd() + '/schedules2.xlsx') as writer:  
        df.to_excel(writer, sheet_name='Sheet1',index=False)


