#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 10:15:12 2021

@author: janinedevera
"""

import pandas as pd
import numpy as np
from geopy.distance import geodesic
from fuzzywuzzy import fuzz
from datetime import datetime 
from datetime import date 

rdb = pd.read_csv("../data/requests_database.csv")
sdb = pd.read_csv("../data/support_database.csv")


## MATCHING SCORES

# Matching string (Category, Option, Additional Info)
df_list = [rdb, sdb]

for df in df_list:
    df["string"] = (df["Cat"] + 
                    df["Opt"].fillna('') +
                    df["AddInfo"].fillna('').replace("NONE","")).astype(str)

# Calculate scores 
pairs_df = pd.DataFrame(
    columns = ["rdb_transactionID", 
               "rdb_userID", 
               "rdb_username", 
               "rdb_string",
               "sdb_transactionID", 
               "sdb_userID", 
               "sdb_username", 
               "sdb_string"])

scores_df = pd.DataFrame(
    columns = ["textScores", 
               "DateDiff", 
               "TimeDiff", 
               "orgDistance", 
               "destDistance"])
    
for r in range(len(rdb)):
    scores = []
    dates = []
    times = []
    orgDist = []
    destDist = []

# LEVEL 1: Generate text similarity scores (for each pair)        
    for s in range(len(sdb)):
        score = fuzz.partial_ratio(rdb.string[r].lower(), 
                                   sdb.string[s].lower())
        scores.append(score)
    
# LEVEL 2: Generate date difference and time difference (for each pair)      
        date = abs((datetime.strptime(rdb.Date[r], '%Y-%m-%d') 
                        - datetime.strptime(sdb.Date[s], '%Y-%m-%d')).days)
        dates.append(date)
            
        time = abs((datetime.strptime(rdb.Time[r], '%H:%M:%S') -  
                    datetime.strptime(sdb.Time[s], '%H:%M:%S')).total_seconds() / 60)
        times.append(time)
    
# LEVEL 3: Generate location (origin) differences (for each pair)
        a = rdb.OrgCoord[r].strip('()').split(',')
        a = tuple(a)
        a = (float(a[0]), float(a[1]))
            
        b = sdb.OrgCoord[s].strip('()').split(',')
        b = tuple(b)
        b = (float(b[0]), float(b[1]))
    
        orgDist.append(geodesic(a, b).kilometers)
            
# LEVEL 3: Generate location (destination) differences (for each pair)  
        if isinstance(rdb.DestCoord[r], float) == False:
            a = rdb.DestCoord[r].strip('()').split(',')
            a = tuple(a)
            a = (float(a[0]), float(a[1]))
        if isinstance(sdb.DestCoord[s], float) == False:
            b = sdb.DestCoord[s].strip('()').split(',')
            b = tuple(b)
            b = (float(b[0]), float(b[1]))
        try:
            distance = geodesic(a, b).kilometers
            destDist.append(distance)
        except ValueError:
            destDist.append("NA")
    
# Helper-helpee dataframe with scores   
        pairs_df = pairs_df.append({'rdb_transactionID':rdb.transactionID[r],
                                    'rdb_userID':rdb.userID[r],
                                    'rdb_username':rdb.username[r],
                                    'rdb_string':rdb.string[r],
                                    'sdb_transactionID':sdb.transactionID[s],
                                    'sdb_userID':sdb.userID[s],
                                    'sdb_username':sdb.username[s],
                                    'sdb_string':sdb.string[s]},
                                   ignore_index=True)
            
    scores_df = scores_df.append({'textScores':scores,
                                  'DateDiff': dates,
                                  'TimeDiff': times,
                                  'orgDistance': orgDist,
                                  'destDistance': destDist},
                                  ignore_index=True)
            
    scores_df = scores_df.explode(['textScores', 'DateDiff', 'TimeDiff',
                                   'orgDistance', 'destDistance'])

pairdb = pd.concat([pairs_df.reset_index(drop=True), 
                      scores_df.reset_index(drop=True)], axis=1)
    

## GENERATE MATCHES

stringThreshold = 90

    # get scores above threshold
match1 = pairdb.loc[pairdb['textScores'] >= stringThreshold]
    
    # get minimum date difference
idx_m2 = match1.groupby(['rdb_transactionID'])['DateDiff'].transform(min) == match1['DateDiff']
match2 = match1[idx_m2]
    
    # get minimum time difference
idx_m3 = match2.groupby(['rdb_transactionID'])['TimeDiff'].transform(min) == match2['TimeDiff']
match3 = match2[idx_m3]
    
    # get minimum location difference (origin)
idx_m4 = match3.groupby(['rdb_transactionID'])['orgDistance'].transform(min) == match3['orgDistance']
match4 = match3[idx_m4]
    
    # get minimum location difference (destination)
idx_m5 = match4.groupby(['rdb_transactionID'])['destDistance'].transform(min) == match4['destDistance']
matches = match4[idx_m5] 

def GetMatch():
    userType = str(input("Did you:" +
                         "\n1. Request for Help" +
                         "\n2. Offer to Help\n" +
                         "\nEnter 1 or 2: "))

    transID = input("What is your transaction ID? ")

    try:
        if userType == "1":
            matchID = matches.loc[matches['rdb_transactionID'] == int(transID)].sdb_transactionID
            matchFinal = sdb.loc[sdb['transactionID'] == int(matchID)]
        else:
            matchID = matches.loc[matches['sdb_transactionID'] == int(transID)].rdb_transactionID
            matchFinal = rdb.loc[rdb['transactionID'] == int(matchID)]
            
    except TypeError:
        print("Sorry, we have not yet found any matches for your request.")
        
    print("Congratulations! You have been matched with: " +
          "\n User: " + str(matchFinal.iloc[0].username) +
          "\n Request Category: " + str(matchFinal.iloc[0].Cat) +
          "\n Request Option: " + str(matchFinal.iloc[0].Opt) +
          "\n Request Origin: " + str(matchFinal.iloc[0].Org) +
          "\n Request Destination: " + str(matchFinal.iloc[0].Dest) +
          "\n Request Date: " + str(matchFinal.iloc[0].Date) +
          "\n Request Time: " + str(matchFinal.iloc[0].Time) +
          "\n Additional Information: " + str(matchFinal.iloc[0].AddInfo) +
          "\n Thank you for using GetHelp!"
              )
          
GetMatch()

