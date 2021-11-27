#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 10:15:12 2021

@author: janinedevera
"""

import pandas as pd
from geopy.distance import geodesic
from fuzzywuzzy import fuzz

rdb = pd.read_csv("../data/requests_databasev1.csv")
sdb = pd.read_csv("../data/support_databasev1.csv")

## Matching
# Step 1: Create string for Category, Option, Date, Time
df_list = [rdb, sdb]

for df in df_list:
    id = []
    for i in range(len(df)):
        id.append(i+1)
    df["transactionID"] = id # create unique transaction ID 
    df["string"] = df.iloc[:,2].astype(str) + df.iloc[:,3].astype(str) + df.iloc[:,4] + df.iloc[:,5].fillna('')

# Step 2: For each observation in rdb, calculate fuzz ratio with all observations in sdb
match_list = []
for x in range(len(rdb)):
    scores = []
    for y in range(len(sdb)):
        score = fuzz.ratio(rdb.string[x],sdb.string[y])
        scores.append(score)

    max_index = scores.index(max(scores))     # get index of maximum score
    match = sdb.iloc[max_index,]              # get row details of match
    match_list.append(match.transactionID)    # get transaction ID of match
    
rdb["matchID"] = match_list

