#!/usr/bin/env python
# coding: utf-8
"""
Created on Mon Dec 16 20:06 2019

@author: Andy St. Jean
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import time
import sys

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# converts the team stat row into a dictionary
# parameter: game_row - html table row containing team stats
# returns: a dictionary containing the team stats from game_row
def create_game_dict(game_row):
    game_dict = {}

    #put the game into a dictionary
    for td in game_row.find_all('td'):
        #want to skip the row with x
        if(td['data-stat'] != 'x'):
            key = td["data-stat"]

            #some preprocessing to mark the game as home or away
            if(key == 'game_location'):
                value = 'H' if td.text == '' else 'A'
            else:
                value = td.text

            game_dict[key] = value
        else:
            continue

    #return the dictionary (MAKE SURE THIS OUTSIDE OF THE FOR LOOP)
    return game_dict

# initialize the data frame with the columns of html table
#parameter: header - an th HTML element holding the column names
#returns: an empty DataFrame with the headers put into column names
def create_game_dataframe(table):
    #get the header and column names
    header = table.find('thead').find_all('tr')[1]
    #get the column headers and do some cleaning
    stat_columns = [c['data-stat'] for c in header.find_all('th') if c['data-stat'] != 'x']
    #load the column headers into a dataframe and remove the ranker header
    return pd.DataFrame(columns=stat_columns[1:])

# Takes a basketball reference team gamelog url and converts it to a dataframe
# parameter: url: the url for basketball reference gamelog page
# returns: a dataframe of the html table
def convert_gamelog_to_dataframe(abv, season):
    url = "https://www.basketball-reference.com/teams/{}/{}/gamelog-advanced/"
    url = url.format(abv, season)

    soup = BeautifulSoup(urlopen(url), 'html.parser')
    table = soup.find('table', {'id':'tgl_advanced'})

    #initialize the dataframe
    game_frame = create_game_dataframe(table)

    #get the table rows
    body = table.find('tbody')
    games = [r for r in body.find_all('tr') if r.has_attr('id')]

    #for each row in the table -> convert to dictionary and add to dataframe
    for g in games:
        game_dict = create_game_dict(g)
        game_frame = game_frame.append(game_dict, ignore_index=True)

    game_frame.insert(1, "id", abv)

    return game_frame


if __name__ == "__main__":

    url = "https://www.basketball-reference.com/teams/BOS/2019/gamelog-advanced/"

    soup = BeautifulSoup(urlopen(url), 'html.parser')
    table = soup.find('table', {'id':'tgl_advanced'})

    print(table)
