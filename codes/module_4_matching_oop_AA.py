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

## MATCHING SCORES
def PrintMatch(mFinal):
    print("Congratulations! You have been matched with: " +
             "\n User: " + str(mFinal.iloc[0].username) +
             "\n Request Category: " + str(mFinal.iloc[0].Cat) +
             "\n Request Option: " + str(mFinal.iloc[0].Opt) +
             "\n Request Origin: " + str(mFinal.iloc[0].Org) +
             "\n Request Destination: " + str(mFinal.iloc[0].Dest) +
             "\n Request Date: " + str(mFinal.iloc[0].Date) +
             "\n Request Time: " + str(mFinal.iloc[0].Time) +
             "\n Additional Information: " + str(mFinal.iloc[0].AddInfo) +
             "\n Thank you for using GetHelp!"
                 )

# Matching string (Category, Option, Additional Info)
class Matches:
    def __init__(self, pairdb = pd.DataFrame(), matches = pd.DataFrame()):
        self.rdb = pd.read_csv("../data/requests_database.csv", dtype = {"transactionID": "str", "userID": "str", "helpID": "str"})
        self.sdb = pd.read_csv("../data/support_database.csv", dtype = {"transactionID": "str", "userID": "str", "helpID": "str"})
        self.pairdb = pairdb
        self.matches = matches
        
    def genpairdb(self):
        df_list = [self.rdb, self.sdb]
        
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
            
        for r in range(len(self.rdb)):
            scores = []
            dates = []
            times = []
            orgDist = []
            destDist = []
        
        # LEVEL 1: Generate text similarity scores (for each pair)        
            for s in range(len(self.sdb)):
                score = fuzz.partial_ratio(self.rdb.string[r].lower(), 
                                           self.sdb.string[s].lower())
                scores.append(score)
            
        # LEVEL 2: Generate date difference and time difference (for each pair)      
                date = abs((datetime.strptime(self.rdb.Date[r], '%Y-%m-%d') 
                                - datetime.strptime(self.sdb.Date[s], '%Y-%m-%d')).days)
                dates.append(date)
                    
                time = abs((datetime.strptime(self.rdb.Time[r], '%H:%M:%S') -  
                            datetime.strptime(self.sdb.Time[s], '%H:%M:%S')).total_seconds() / 60)
                times.append(time)
            
        # LEVEL 3: Generate location (origin) differences (for each pair)
                a = tuple(self.rdb.OrgCoord[r].strip('()').split(','))
                a = (float(a[0]), float(a[1]))
                    
                b = tuple(self.sdb.OrgCoord[s].strip('()').split(','))
                b = (float(b[0]), float(b[1]))
            
                orgDist.append(geodesic(a, b).kilometers)
                    
        # LEVEL 3: Generate location (destination) differences (for each pair)  
                if isinstance(self.rdb.DestCoord[r], float) == False:
                    a = tuple(self.rdb.DestCoord[r].strip('()').split(','))
                    a = (float(a[0]), float(a[1]))
                if isinstance(self.sdb.DestCoord[s], float) == False:
                    b = tuple(self.sdb.DestCoord[s].strip('()').split(','))
                    b = (float(b[0]), float(b[1]))
                try:
                    distance = geodesic(a, b).kilometers
                    destDist.append(distance)
                except ValueError:
                    destDist.append("NA")
            
        # Helper-helpee dataframe with scores   
                pairs_df = pairs_df.append({'rdb_transactionID':self.rdb.transactionID[r],
                                            'rdb_userID':self.rdb.userID[r],
                                            'rdb_username':self.rdb.username[r],
                                            'rdb_string':self.rdb.string[r],
                                            'sdb_transactionID':self.sdb.transactionID[s],
                                            'sdb_userID':self.sdb.userID[s],
                                            'sdb_username':self.sdb.username[s],
                                            'sdb_string':self.sdb.string[s]},
                                           ignore_index=True)
                    
            scores_df = scores_df.append({'textScores':scores,
                                          'DateDiff': dates,
                                          'TimeDiff': times,
                                          'orgDistance': orgDist,
                                          'destDistance': destDist},
                                          ignore_index=True)
                    
            scores_df = scores_df.explode(['textScores', 'DateDiff', 'TimeDiff',
                                           'orgDistance', 'destDistance'])
        
        self.pairdb = pd.concat([pairs_df.reset_index(drop=True), 
                              scores_df.reset_index(drop=True)], axis=1)
        
        # drop matches to itself
        self.pairdb = self.pairdb.drop(self.pairdb[self.pairdb.rdb_userID == self.pairdb.sdb_userID].index)
  
    def getpairdb(self):
        return self.pairdb
       
    def genMatchesdb(self):
        ## GENERATE MATCHES
        stringThreshold = 90
        
            # get scores above threshold
        match1 = self.pairdb.loc[self.pairdb['textScores'] >= stringThreshold]
            
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
        self.matches = match4[idx_m5] 
        
    def getMatchesdb(self):
        return self.matches
    
    def getMatch(self):
        userType = str(input("Did you:" +
                             "\n1. Request for Help" +
                             "\n2. Offer to Help\n" +
                             "\nEnter 1 or 2: "))
    
        transID1 = str(input("What is your transaction ID? ")) # renamed because there's a transID function in Module 3
        # try "00001100001" for userType 1 - not yet matched
        # try "00014200001" for userType 2 - has multiple matches
        # try any number not transactionID - invalid ID
    
        if userType == "1":
            if (self.pairdb.rdb_transactionID.isin([transID1]).any()): #if transID1 exists
                if (self.matches.rdb_transactionID.isin([transID1]).any()): #if transID1 has match
                    matchID = self.matches.loc[self.matches['rdb_transactionID'] == str(transID1)].sdb_transactionID
                    matchFinal = self.sdb[self.sdb.transactionID.isin(matchID.tolist())] # there can be multiple matchID
                    PrintMatch(matchFinal)
                else: #if transID1 has no match
                    print("Sorry, we have not yet found any matches for your request.")           
            else: # if transID1 does not match
                print("Sorry, the transaction ID does not exist.")
                
        elif userType == "2":
            if (self.pairdb.sdb_transactionID.isin([transID1]).any()): #if transID1 exists
                if (self.matches.sdb_transactionID.isin([transID1]).any()): #if transID1 has match
                    matchID = self.matches.loc[self.matches['sdb_transactionID'] == str(transID1)].rdb_transactionID
                    matchFinal = self.rdb[self.rdb.transactionID.isin(matchID.tolist())] #there can be multiple matches
                    PrintMatch(matchFinal)
                else: #if transID1 has no match
                    print("Sorry, we have not yet found any matches for your request.")           
            else: # if transID1 does not match
                print("Sorry, the transaction ID does not exist.")
        
        else:
            print("Please enter a valid option.")
            Matches.getMatch(self)

m=Matches()
m.genpairdb()
m.genMatchesdb()
m.getpairdb()
m.getMatchesdb()
m.getMatch()
