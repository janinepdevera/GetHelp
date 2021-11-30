#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 10:15:12 2021

@author: janinedevera
"""

import pandas as pd
from geopy.distance import geodesic
from fuzzywuzzy import fuzz

rdb = pd.read_csv("./data/requests_database.csv")
sdb = pd.read_csv("./data/support_database.csv")

# MATCHING

# 1. Create matching string (Category, Option, Additional Info)

df_list = [rdb, sdb]

for df in df_list:
    df["string"] = (df["Cat"] + df["Opt"].fillna('') +
                    df["AddInfo"].fillna('')).astype(str)

# 2. Generate text similarity scores (rdb vs sdb)

matches_cols = ["rdb_transactionID", "rdb_userID", "rdb_username", "rdb_string",
                "sdb_transactionID", "sdb_userID", "sdb_username", "sdb_string"]
matches_df = pd.DataFrame(columns = matches_cols)

scores_df = pd.DataFrame(columns = ["textScores"])

for r in range(len(rdb)):
    scores = []
    for s in range(len(sdb)):
        score = fuzz.partial_ratio(rdb.string[r].lower(), sdb.string[s].lower())
        scores.append(score)

# 3. Create dataframe of all helper-helpee pairs  
        matches_df = matches_df.append({'rdb_transactionID':rdb.transactionID[r],
                                        'rdb_userID':rdb.userID[r],
                                        'rdb_username':rdb.username[r],
                                        'rdb_string':rdb.string[r],
                                        'sdb_transactionID':sdb.transactionID[s],
                                        'sdb_userID':sdb.userID[s],
                                        'sdb_username':sdb.username[s],
                                        'sdb_string':sdb.string[s]},
                                        ignore_index=True)
      
    scores_df = scores_df.append({'textScores':scores},
                                    ignore_index=True)
        
    scores_df = scores_df.explode('textScores')
    
match1 = pd.concat([matches_df.reset_index(drop=True), 
                    scores_df.reset_index(drop=True)], 
                   axis=1)

            

    
### OLD CODES ###

#scores_list = []
#match_list = []
#match_string = []

#for r in range(len(rdb)):
    scores = []
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

# Matching with distance:
# DO NOT RUN

#rdb_Ride = rdb.loc[rdb["Cat"] == "Ride"]
#sdb_Ride = sdb.loc[sdb["Cat"] == "Ride"]


# for r in range(len(rdb_Ride)):
#scores = []
#distDiff = []
# for s in range(len(sdb_Ride)):
#score = fuzz.ratio(rdb_Ride.string[r],sdb_Ride.string[s])
# scores.append(score)

#diff = float(rdb_Ride.distanceKM[r]) - float(sdb_Ride.distanceKM[s])
# distDiff.append(diff)

# 2. Create distance variable
#distance =[]

# for i in range(len(df)):
# if isinstance(df.OrgCoord[i], float) == True:
# distance.append("NA")

# else:

#a = df.OrgCoord[i].strip('()').split(',')
#a = tuple(a)
#a = (float(a[0]), float(a[1]))

#b = df.DestCoord[i].strip('()').split(',')
#b = tuple(b)
#b = (float(b[0]), float(b[1]))

#distance.append(geodesic(a, b).kilometers)

#df["distanceKM"] = distance
