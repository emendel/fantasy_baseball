import time
import csv
from datetime import date, timedelta
import datetime
import shutil
import pandas as pd




TEAMS = {
    'NYY': ['Gerrit Cole', 'Carlos Rodon', 'Nestor Cortes', 'Luis Severino', 'Frankie Montas']
}


# with open('rotation.csv', 'w', newline='') as csvfile:
#     for team in TEAMS:
#         writer = csv.writer(csvfile)
#         writer.writerow([team] + results[team])



with open ('schedules_rotation.csv', 'w', newline='') as csvfile:
    with open('schdules.csv', 'r') as f:         
         # Read lines separately
        reader = csv.reader(f, delimiter=',')
        for i, line in enumerate(reader):
            cnt = 0
            if line[0] == 'NYY' and i % 2 == 1:
                writer = csv.writer(csvfile)
                writer.writerow(line)
            elif line[0] == 'NYY' and i % 2 == 0:
                writer = csv.writer(csvfile)
                writer.writerow(['NYY'] + TEAMS[line[0]]*6)
                print(i, line)