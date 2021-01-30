import csv

with open('export.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row, '\n')

print('\nFinished!\n')