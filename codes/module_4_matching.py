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

# MATCHING

# 1. Create matching string (Category, Option, Additional Info)

df_list = [rdb, sdb]

for df in df_list:
    df["string"] = (df["Cat"] + df["Opt"].fillna('') +
                    df["AddInfo"].fillna('').replace("NONE","")).astype(str)

# 2. Prepare dataframe of all helper-helpee pairs 

pairs_cols = ["rdb_transactionID", "rdb_userID", "rdb_username", "rdb_string",
                "sdb_transactionID", "sdb_userID", "sdb_username", "sdb_string"]
pairs_df = pd.DataFrame(columns = pairs_cols)

scores_df = pd.DataFrame(columns = ["textScores", "DateDiff", "TimeDiff",
                                    "orgDistance", "destDistance"])

# 3. LEVEL 1: Generate text similarity scores (for each pair)

for r in range(len(rdb)):
    
    scores = []
    dates = []
    times = []
    orgDist = []
    destDist = []
    
    for s in range(len(sdb)):
        score = fuzz.partial_ratio(rdb.string[r].lower(), sdb.string[s].lower())
        scores.append(score)

# 4. LEVEL 2: Generate date difference and time difference (for each pair)   
  
        date = abs((datetime.strptime(rdb.Date[r], '%Y-%m-%d') 
                    - datetime.strptime(sdb.Date[s], '%Y-%m-%d')).days)
        dates.append(date)
        
        time = abs((datetime.strptime(rdb.Time[r], '%H:%M:%S') -  
                datetime.strptime(sdb.Time[s], '%H:%M:%S')).total_seconds() / 60)
        times.append(time)

# 5. LEVEL 3: Generate location (origin) differences (for each pair)

        a = rdb.OrgCoord[r].strip('()').split(',')
        a = tuple(a)
        a = (float(a[0]), float(a[1]))
        
        b = sdb.OrgCoord[s].strip('()').split(',')
        b = tuple(b)
        b = (float(b[0]), float(b[1]))

        orgDist.append(geodesic(a, b).kilometers)
        
# 6. LEVEL 3: Generate location (destination) differences (for each pair)

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


# 7. Populate helper-helpee dataframe with scores

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
    
match_df = pd.concat([pairs_df.reset_index(drop=True), 
                    scores_df.reset_index(drop=True)], axis=1)

# 8. Generate matches

def unique(list1):
    x = np.array(list1)
    print(np.unique(x))

stringThreshold = 90

def GetMatch():
    
## Dataframe of final matches    
    # get scores above threshold
    match1 = match_df.loc[match_df['textScores'] >= stringThreshold]
    
    # get minimum data difference
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
    match5 = match4[idx_m5]
    
    
## Return match to user
    userType = str(input("Did you:" +
                         "\n1. Request for Help" +
                         "\n2. Offer to Help\n" +
                         "\nEnter 1 or 2: "))

    transID = int(input("What is your transaction ID? "))
    
    if userType == "1":
        matchID = int(match5.loc[match5['rdb_transactionID'] == transID].sdb_transactionID)
        matchFinal = sdb.loc[sdb['transactionID'] == matchID]
        
    else:
        matchID = int(match5.loc[match5['sdb_transactionID'] == transID].rdb_transactionID)
        matchFinal = rdb.loc[rdb['transactionID'] == matchID]


    #print("Congratulations! You have been matched with: " +
          #"\n User ID: " + str(sdbMatch.iloc[0].userid) +
          #"\n Request Category: " + str(sdbMatch.iloc[0].Cat) +
          #"\n Request Option: " + str(sdbMatch.iloc[0].Opt) +
          #"\n Request Origin: " + str(sdbMatch.iloc[0].Org) +
          #"\n Request Destination: " + str(sdbMatch.iloc[0].Dest) +
          #"\n Request Date: " + str(sdbMatch.iloc[0].Date) +
          #"\n Request Time: " + str(sdbMatch.iloc[0].Time) +
          #"\n Thank you for using GetHelp!"
          #)
          
GetMatch()



### OLD CODES ###

#scores_list = []
#match_list = []
#match_string = []

#for r in range(len(rdb)):
    #scores = []
    #for s in range(len(sdb)):
        #score = fuzz.ratio(rdb.string[r], sdb.string[s])
        # create list of scores for each obs
        #scores.append(score)

    # create list of max scores per obs
    #scores_list.append(max(scores))
    #max_index = scores.index(max(scores))     # get index of maximum score
    #match = sdb.iloc[max_index, ]              # get row details of match
    #match_list.append(match.transactionID)    # get transaction ID of match
    #match_string.append(match.string)         # get details of match

#rdb["matchID"] = match_list
#rdb["matchScores"] = scores_list
#rdb["matchString"] = match_string

# 2. Print details of match: userID + details
# Still need to generate errors for invalid Transaction IDs
# Can this be included as method in Request class?

#userType = str(input("Did you:" +
                     #"\n1. Request for Help" +
                     #"\n2. Offer to Help\n" +
                     #"\nEnter 1 or 2: "))
#transID = int(input("What is your transaction ID? "))

#matchID = int(rdb.loc[rdb['transactionID'] == transID].matchID)
#sdbMatch = sdb.loc[sdb["transactionID"] == matchID]

#print("Congratulations! You have been matched with: " +
      #"\n User ID: " + str(sdbMatch.iloc[0].userid) +
      #"\n Request Category: " + str(sdbMatch.iloc[0].Cat) +
      #"\n Request Option: " + str(sdbMatch.iloc[0].Opt) +
      #"\n Request Origin: " + str(sdbMatch.iloc[0].Org) +
      #"\n Request Destination: " + str(sdbMatch.iloc[0].Dest) +
      #"\n Request Date: " + str(sdbMatch.iloc[0].Date) +
      #"\n Request Time: " + str(sdbMatch.iloc[0].Time) +
      #"\n Thank you for using GetHelp!"
      #)

