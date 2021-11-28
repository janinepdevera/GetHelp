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

## Dataframe preparations:  
df_list = [rdb, sdb]

for df in df_list:
    
    # 1. Create unique transaction ID
    ## This can be provided after every to user after every input
    id = []
    for i in range(len(df)):
        id.append(i+1)
    df["transactionID"] = id

    # 2. Create distance variable 
    distance =[]

    for i in range(len(df)):
        if isinstance(df.OrgCoord[i], float) == True:
            distance.append("NA")
        
        else:
    
            a = df.OrgCoord[i].strip('()').split(',')
            a = tuple(a)
            a = (float(a[0]), float(a[1]))
        
            b = df.DestCoord[i].strip('()').split(',')
            b = tuple(b)
            b = (float(b[0]), float(b[1]))
    
            distance.append(geodesic(a, b).kilometers)

    df["distanceKM"] = distance

    # 3. Create matching string (Category, Option, Date, Time)
    df["string"] = df["Cat"] + df["Opt"].fillna('') + df["Date"] + df["Time"]


## Matching:

    # 1. For each observation in rdb, calculate fuzz ratio vs all observations in sdb
    ## Still need to generate matches in sdb dataframe
    
scores_list = []
match_list = []
match_string = []
for x in range(len(rdb)):
    scores = []
    for y in range(len(sdb)):
        score = fuzz.ratio(rdb.string[x],sdb.string[y])
        scores.append(score)                  # create list of scores for each obs

    scores_list.append(max(scores))           # create list of max scores per obs
    max_index = scores.index(max(scores))     # get index of maximum score
    match = sdb.iloc[max_index,]              # get row details of match
    match_list.append(match.transactionID)    # get transaction ID of match
    match_string.append(match.string)         # get details of match
    
rdb["matchID"] = match_list
rdb["matchScores"] = scores_list
rdb["matchString"] = match_string

    # 2. Print details of match: userID + details 
    ## Can be included as a method to Request class?

userType = str(input("Did you:" +
                         "\n1. Request for Help" + 
                         "\n2. Offer to Help\n" +
                         "\nEnter 1 or 2: "))   
transID = int(input("What is your transaction ID? "))

matchID = int(rdb.loc[rdb['transactionID'] == transID].matchID)
sdbMatch = sdb.loc[sdb["transactionID"] == matchID]

print("Congratulations you have been matched with: " +
      "\n User ID: " + str(sdbMatch.at[0, 'userid']) +
      "\n Request Category: " + sdbMatch.at[0, 'Cat'] +
      "\n Request Option: " + str(sdbMatch.at[0, 'Opt']) +
      "\n Request Origin: " + sdbMatch.at[0, 'Org'] + 
      "\n Request Destination: " + sdbMatch.at[0, 'Dest'] + 
      "\n Request Date: " + str(sdbMatch.at[0, 'Date']) + 
      "\n Request Time: " + str(sdbMatch.at[0, 'Time'])
      )
    

    
