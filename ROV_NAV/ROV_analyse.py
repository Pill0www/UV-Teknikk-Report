import numpy as np
import matplotlib.pyplot
import csv

def read_file(filename):
    data = {}
    title = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        indeks = 0
        for line in reader:
            split_line = line.split(",")
            title_number = 0
            if indeks == 0:
                for i in range(len(split_line)):
                    data[split_line[i]] = []
                    title.append(split_line[i])
                indeks += 1
        
            else:
                for i in range(len(split_line)):
                    data[title[i]].append(split_line[i])

    return data



