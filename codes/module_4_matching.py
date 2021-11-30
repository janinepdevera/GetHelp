#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 10:15:12 2021

@author: janinedevera
"""

import pandas as pd
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
                    df["AddInfo"].fillna('')).astype(str)

# 2. Prepare dataframe of all helper-helpee pairs 

matches_cols = ["rdb_transactionID", "rdb_userID", "rdb_username", "rdb_string",
                "sdb_transactionID", "sdb_userID", "sdb_username", "sdb_string"]
matches_df = pd.DataFrame(columns = matches_cols)

scores_df = pd.DataFrame(columns = ["textScores", "DateDiff", "TimeDiff",
                                    "orgDistance"])

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
  
        # remove time difference
        date = datetime.strptime(rdb.Date[r], '%Y-%m-%d') - datetime.strptime(sdb.Date[s], '%Y-%m-%d')
        dates.append(date)
        
        # remove day difference
        time = datetime.strptime(rdb.Time[r], '%H:%M:%S') -  datetime.strptime(sdb.Time[s], '%H:%M:%S')
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

# 7. Populate helper-helpee dataframe with scores

        matches_df = matches_df.append({'rdb_transactionID':rdb.transactionID[r],
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
                                 'orgDistance': orgDist},
                                 ignore_index=True)
        
    scores_df = scores_df.explode(['textScores', 'DateDiff', 'TimeDiff', 'orgDistance'])
    
match_final = pd.concat([matches_df.reset_index(drop=True), 
                    scores_df.reset_index(drop=True)], 
                   axis=1)

# 8. Match using text score, date and time difference, OD differences            

# 9. Print details of match    





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

