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
    
    df.rename(columns={df.columns[0]:'userid',
                       df.columns[1]:'userType',
                       df.columns[2]:'Date',
                       df.columns[3]:'Time',
                       df.columns[4]:'Cat',
                       df.columns[5]:'Opt',
                       df.columns[6]:'Org',
                       df.columns[7]:'OrgAdd',
                       df.columns[8]:'OrgCoord',
                       df.columns[9]:'Dest',
                       df.columns[10]:'DestAdd',
                       df.columns[11]:'DestCoord'},
              inplace = True)
    
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
    ## Still need to save matches in sdb dataframe

scores_list = []
match_list = []
match_string = []

for r in range(len(rdb)):
    scores = []
    for s in range(len(sdb)):
        score = fuzz.ratio(rdb.string[r],sdb.string[s])
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
    ## Still need to generate errors for invalid Transaction IDs
    ## Can this be included as method in Request class? 

userType = str(input("Did you:" +
                         "\n1. Request for Help" + 
                         "\n2. Offer to Help\n" +
                         "\nEnter 1 or 2: "))   
transID = int(input("What is your transaction ID? "))

matchID = int(rdb.loc[rdb['transactionID'] == transID].matchID)
sdbMatch = sdb.loc[sdb["transactionID"] == matchID]

print("Congratulations! You have been matched with: " +
      "\n User ID: " + str(sdbMatch.iloc[0].userid) +
      "\n Request Category: " + str(sdbMatch.iloc[0].Cat) +
      "\n Request Option: " + str(sdbMatch.iloc[0].Opt) +
      "\n Request Origin: " + str(sdbMatch.iloc[0].Org) + 
      "\n Request Destination: " + str(sdbMatch.iloc[0].Dest) + 
      "\n Request Date: " + str(sdbMatch.iloc[0].Date) + 
      "\n Request Time: " + str(sdbMatch.iloc[0].Time) +
      "\n Thank you for using GetHelp!"
      )

## Matching with distance: 
### DO NOT RUN

#rdb_Ride = rdb.loc[rdb["Cat"] == "Ride"]
#sdb_Ride = sdb.loc[sdb["Cat"] == "Ride"]


#for r in range(len(rdb_Ride)):
    #scores = []
    #distDiff = []
    #for s in range(len(sdb_Ride)):
        #score = fuzz.ratio(rdb_Ride.string[r],sdb_Ride.string[s])
        #scores.append(score)                 

        #diff = float(rdb_Ride.distanceKM[r]) - float(sdb_Ride.distanceKM[s])                  
        #distDiff.append(diff)    

    
