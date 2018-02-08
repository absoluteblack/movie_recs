import numpy as np
from functools import reduce
import csv

def get_dictionary(filename):

    dictionary = []
    with open(filename) as csvfile:
        movie_reader = csv.DictReader(csvfile)
        dictionary = list(map(lambda row: row, movie_reader))
    return dictionary

def get_column(dictionary, column):
    return list(map(lambda e: e[column], dictionary))

def get_columns(dictionary, columns):
    return list(zip(*list(map(lambda c: get_column(dictionary, c), columns))))

def get_group_weighting(num_seen, group_size, group_size_weighting = 2):

    num = group_size / 2
    score = num_seen - num
    score = score ** 2
    score = score * -1
    score = score / (2 * group_size_weighting)
    score = np.exp(score)
    score = 1 / (np.sqrt( 2 * np.pi * group_size_weighting)) * score
    return score

def get_movie_averages(dictionary, columns):

    rotated_dict = get_columns(dictionary, columns)
    processed_dict = list(map(lambda r: list(map(lambda e: int(e), list(filter(lambda e: e.isdigit() and e != '0', r)))), rotated_dict))
    averages = list(map(lambda r: sum(r)/len(r), processed_dict))
    return averages

def get_score(row, group_size, group_size_weighting):

    average = row[-1]
    group_weighting_scale = get_group_weighting(len(row) - 1, group_size, group_size_weighting)
    return float(average) * float(group_weighting_scale)

def get_max(dictionary, index):
    return list(reduce(lambda r,y: r if r[index] > y[index] else y, dictionary))

def get_scores(filename = 'movies.csv', names = [], group_size_weighting = 2):

    dictionary = get_dictionary(filename)
    top_row = list(dictionary[0].keys())
    averages = get_movie_averages(dictionary, top_row)

    columns = []
    if names == []:
        columns = top_row
    else:
        columns.append(top_row[0])
        columns += names
    group_size = len(columns) - 1

    relevant_dict = get_columns(dictionary, columns[1:])
    processed_dict = list(map(lambda r: list(map(lambda e: int(e), list(filter(lambda e: e != '0' and e != '', r)))), relevant_dict))
    dict_with_averages = list(map(lambda r: list(r[0]) + [r[1]], list(zip(processed_dict, averages))))
    titles = get_column(dictionary, columns[0])
    scores = list(map(lambda r: get_score(r, group_size, group_size_weighting), dict_with_averages))
    return list(zip(titles, scores))

