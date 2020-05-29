import requests
import json
import re
from time import sleep
import numpy as np
import matplotlib.pyplot as plt

def get_url(place):
    return "https://geocode.xyz/" + place + "?json=1"

data = []

def uni2ascii(x):
    x = list(x)
    for idx, c in enumerate(x):
        if c == "ö" or c == "Ö":
            x[idx] = "o"
        if c == "İ" or c == "ı" or c == "I":
            x[idx] = "i"
        if c == "Ç" or c == "ç":
            x[idx] = "c"
        if c == "Ü" or c == "ü":
            x[idx] = "u"
        if c == "Ğ" or c == "ğ":
            x[idx] = "g"
        if c == "Ş" or c == "ş":
            x[idx] = "s"
        
    
    return "".join(x)


with open("population_density_time_period.csv", "r") as f:
    next(f)
    for line in f:
        
        splitted = [uni2ascii(x) for x in line.split(",")]
        
        try:
            place = re.match('"([A-Za-z0-9 -\.]+)"', splitted[2]).group(1).strip()
        except AttributeError:
            place = re.match('"([A-Za-z0-9 -\.]+)"', splitted[3]).group(1).strip()

        pop = int(re.match('"([0-9]+)"', splitted[4]).group(1))

        data.append([place.lower(), pop])

pops = {}

for row in data:
    if row[0] in pops:
        pops[row[0]] += [row[1]]
    else:
        pops[row[0]] = [ row[1] ]

pop_coord_list = []

for key, val in pops.items():
    median = np.median(val)
    pop_coord_list.append([key, median,])

neig_coord_list = {}

with open("muhtarlik.csv") as f:
    next(f)
    for line in f:
        splitted = [uni2ascii(x) for x in line.split(",")]

        if len(splitted[4]) > 1:
            place = splitted[4].lower().strip()
        else:
            place = splitted[3].lower().strip()
        """
        try:
            place = re.match('"([A-Za-z0-9 -\.]+)"', splitted[4]).group(1)
        except AttributeError:
            place = re.match('"([A-Za-z0-9 -\.]+)"', splitted[3]).group(1)
    
        lat = float(re.match('"([0-9\.]+)"', splitted[7]).group(1))
        lon = float(re.match('"([0-9\.]+)"', splitted[8]).group(1))
        """

        try:
            lat = float(splitted[7])
            lon = float(splitted[8])
        except ValueError:
            continue

        neig_coord_list[place] = [ lat, lon ]

[print(x) for x in neig_coord_list.keys()]
print("*******#####£#####***")

cnt = 0

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

with open("usefull_data.txt", "w") as f:
    for row in pop_coord_list:

        min_acc = 1000000000
        min_name = None

        for key, val in neig_coord_list.items():
            dist = levenshteinDistance(key, row[0])
            acc = dist / (len(key) + len(row[0]))
            if acc < min_acc:
                min_acc = acc
                min_name = key

        acc = min_acc

        if acc < 0.1:
            row[0] = min_name

        try:
            lat, lon = neig_coord_list[row[0]]
        except:
            continue


        f.write( str(row[0]) + "," + str(row[1]) + "," + str(lat) + "," + str(lon) + "\n" )

#response = json.loads(requests.get(get_url(place)).text)
#float(response["latt"]), float(response["longt"])