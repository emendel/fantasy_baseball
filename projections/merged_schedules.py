import csv
file1 = []
with open('rotation.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        file1.append(row)

file2 = []
with open('schdules.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        file2.append(row)

file3 = []

for x in range(0, len(file1)):
    file3.append(file1[x])
    file3.append(file2[x])

with open('merged_schedules.csv', 'w') as csvfile:
    for x in file3:
        writer = csv.writer(csvfile)
        writer.writerow(x)
